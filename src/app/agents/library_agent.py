from src.app.api.models.models import ToolCallResponse
from src.app.api.tools.tool_registry import ToolRegistry
from src.app.llm.base_service import LLMService
from src.app.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    ContextToolOutputItem
)
from src.app.llm.models.llm_response import LLMResponse
from src.app.skills.skill_registry import SkillRegistry

from .utils.exceptions import MaxStepsExceededError
from .utils.prompts import load_prompt

LIBRARY_AGENT_SYSTEM_PROMPT = load_prompt("library_agent_prompt.md")

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
                system_prompt = LIBRARY_AGENT_SYSTEM_PROMPT,
                context_item = context_item, 
                available_tools = self._tool_registry.list_definitions()
            )

            tool_call = response.tool_use
            if response.is_final: # no function calls - agentic loop termination
                responses.append(response.response)
                break
                
            tool_result: ToolCallResponse = await self.mcp.call_tool(tool_name = tool_call.tool_name, tool_args = tool_call.tool_args)

            responses.append(tool_result.log)

            context_item = ContextToolOutputItem(
                tool_call_id=tool_call.call_id,
                tool_output=tool_result.content
            )
        else:
            raise MaxStepsExceededError(f"Agent maximum number of allowed interactions {MAX_STEPS} has been reached!")
        
        return "\n".join(responses)