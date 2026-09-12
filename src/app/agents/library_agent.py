import json

from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    ContextToolOutputItem
)
from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.models.llm_response import LLMResponse
from src.app.domain.prompt.models import Prompt, PromptType
from src.app.observability.event_logger import EventLogger
from src.app.observability.models import EventType
from src.app.prompts.utils.prompts import load_prompt
from src.app.schemas.extracted_book import ExtractedBooks
from src.app.skills.models import Skill
from src.app.tools.tool_registry import ToolRegistry

from .agent import Agent
from .exceptions import MaxStepsExceededError
from .models.models import (
    BooksValidationResult,
    FinishedMonthValidationResult
)
from .utils.utils import (
    prepare_books_insertion,
    validate_extracted_books,
    normalize_finished_month
)

SYSTEM_PROMPT = load_prompt(
    Prompt(
        type=PromptType.AGENT, 
        filename="library_agent_prompt.md"
    )
)

MAX_STEPS = 10

class LibraryAgent(Agent):

    def __init__(
        self, 
        tool_registry: ToolRegistry, 
        llm: LLMService,
        skills: list[Skill],
        event_loger: EventLogger
    ):
        super().__init__(
            name = "library",
            tool_registry = tool_registry,
            llm = llm,
            skills = skills,
            event_logger = event_loger
        )

    async def run(self, prompt: str) -> str:

        await self._log(
            agent=self._name,
            event=EventType.AGENT_START
        )
            
        responses: list[LLMResponse] = []

        context_item = ContextRoleItem(
            role="user",
            content=[
                TextContent(
                    text=prompt
                )
            ]
        )

        for _ in range(MAX_STEPS):
            llm_response: LLMResponse = await self.execute_llm_request(
                context_item=context_item,
                system_prompt=SYSTEM_PROMPT,
                promt=prompt
            )
            responses.append(llm_response.response)

            tool_call = llm_response.tool_use
            if llm_response.is_final: # no function calls - agentic loop termination
                break

            tool_name = tool_call.tool_name
            tool_args = tool_call.tool_args

            if tool_name == "insert_books":
                extracted_books: ExtractedBooks = ExtractedBooks.model_validate(tool_args)
                        
                validation_results: BooksValidationResult = validate_extracted_books(extracted_books.books)

                if not validation_results.valid:
                    validation_results_dict = [result.model_dump() for result in validation_results.results]
                    context_item = ContextToolOutputItem(
                                    tool_call_id = tool_call.call_id,
                                    tool_output = json.dumps(validation_results_dict)
                                )
                    continue

                extracted_validated_books = [result.book for result in validation_results.results]
                books_for_insertion = prepare_books_insertion(extracted_validated_books)

                books_for_insertion_dict = {
                    "books": [book.to_dict() for book in books_for_insertion]
                }

                tool_args = books_for_insertion_dict

            if tool_name == "update_book_finished_month":
                finished_month_validation_result: FinishedMonthValidationResult = normalize_finished_month(tool_args["finished_month"])

                if not finished_month_validation_result.valid:
                    validation_results_dict = finished_month_validation_result.model_dump()
                    context_item = ContextToolOutputItem(
                            tool_call_id = tool_call.call_id,
                            tool_output = json.dumps(validation_results_dict)
                        )
                    continue

                tool_args["finished_month"] = finished_month_validation_result.value

            tool_result: ToolCallResponse = await super().execute_tool(tool_call=tool_call)

            context_item = ContextToolOutputItem(
                tool_call_id=tool_call.call_id,
                tool_output=tool_result.content
            )
        else:
            raise MaxStepsExceededError(f"Agent maximum number of allowed interactions {MAX_STEPS} has been reached!")

        await self._log(
            agent=self._name,
            event=EventType.AGENT_END
        )

        return "\n\n".join(responses)
    