import json

from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    ContextToolOutputItem
)
from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.models.llm_response import LLMResponse
from src.app.domain.book.models import Book
from src.app.domain.prompt.models import Prompt, PromptType
from src.app.domain.prompt.models import Prompt, PromptType
from src.app.prompts.utils.prompts import load_prompt
from src.app.schemas.extracted_book import ExtractedBooks
from src.app.skills.skill_registry import SkillRegistry
from src.app.tools.definitions.tool_definitions import RETRIEVE_RECEIPT_BOOKS_TOOL
from src.app.tools.tool_host import RETRIEVE_RECEIPT_DATA_TOOL
from src.app.tools.tool_registry import ToolRegistry
from src.app.tools.tool_registry import ToolRegistry

from .exceptions import MaxStepsExceededError
from .models.models import BooksValidationResult
from .utils.utils import prepare_books_insertion

SYSTEM_PROMPT = load_prompt(Prompt(type=PromptType.AGENT, filename="library_agent_prompt.md"))

MAX_STEPS = 10

class LibraryAgent:

    def __init__(self, tool_registry: ToolRegistry, skill_registry: SkillRegistry, llm: LLMService):
        self._tool_registry = tool_registry
        self._skill_registry = skill_registry
        self._llm = llm
        

    async def run(self, prompt: str):
        
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

            response: LLMResponse = await self._llm.process(
                system_prompt = SYSTEM_PROMPT,
                context_item = context_item, 
                available_tools = self._tool_registry.list_definitions()
            )

            tool_call = response.tool_use
            if response.is_final: # no function calls - agentic loop termination
                responses.append(response.response)
                break
            
            tool_name = tool_call.tool_name

            # if tool_name == RETRIEVE_RECEIPT_DATA_TOOL.name:
            #     tool_result: ToolCallResponse = await self._tool_registry.execute(
            #         tool_name=tool_name, 
            #         tool_args=tool_call.tool_args,
            #     )

            if tool_name == "insert_books":
                # books_dict: dict = json.loads(tool_call.tool_args)

                extracted_books: ExtractedBooks = ExtractedBooks.model_validate_json(response.response)
                        
                # validation_result: BooksValidationResult = prepare_books_insertion(extracted_books.books)

            tool_result: ToolCallResponse = await self._tool_registry.execute(tool_name=tool_name, tool_args=tool_call.tool_args)

            context_item = ContextToolOutputItem(
                tool_call_id=tool_call.call_id,
                tool_output=tool_result.content
            )
        else:
            raise MaxStepsExceededError(f"Agent maximum number of allowed interactions {MAX_STEPS} has been reached!")
        
        return "\n".join(responses)

    async def handle_insert_books_request(self):

        pass