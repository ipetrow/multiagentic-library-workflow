from src.app.adapters.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    ContextToolOutputItem
) 
from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.llm_response import LLMResponse, ToolUse
from src.app.domain.prompt.models import Prompt, PromptType
from src.app.prompts.utils.prompts import load_prompt
from src.app.skills.models import Skill
from src.app.tools.tool_registry import ToolRegistry

from .agent import Agent
from .exceptions import MaxStepsExceededError

SYSTEM_PROMPT = load_prompt(
    Prompt(
        type=PromptType.AGENT, 
        filename="analysis_agent_prompt.md"
    )
)

MAX_STEPS = 10

class AnalysisAgent(Agent):

    def __init__(
            self, 
            tool_registry: ToolRegistry, 
            llm: LLMService,
            skills: list[Skill]
    ):
        super().__init__(
            _tool_registry = tool_registry,
            _llm = llm,
            _skills = skills
        )
        
    async def run(self, prompt: str) -> str:
                    
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
            llm_response: LLMResponse = await self._llm.process_beta(
                context_item = context_item, 
                skills = self._skills,
                system_prompt = SYSTEM_PROMPT,
                available_tools = self._tool_registry.list_definitions()
            )
            responses.append(llm_response.response)

            tool_call = llm_response.tool_use
            if llm_response.is_final: # no function calls - agentic loop termination
                break

            tool_result: ToolCallResponse = await super().execute_tool(tool_call=tool_call)

            context_item = ContextToolOutputItem(
                tool_call_id=tool_call.call_id,
                tool_output=tool_result.content
            )
        else:
            raise MaxStepsExceededError(f"Agent maximum number of allowed interactions {MAX_STEPS} has been reached!")

        return "\n\n".join(responses)
