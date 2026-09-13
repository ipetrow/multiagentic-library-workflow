from abc import ABC, abstractmethod
from typing import Any

from src.app.adapters.llm.models.models import ContextRoleItem
from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.llm_response import LLMResponse
from src.app.adapters.llm.models.llm_response import ToolUse
from src.app.observability.event_logger import EventLogger
from src.app.observability.models import EventType
from src.app.skills.models import Skill
from src.app.tools.tool_registry import ToolRegistry

class Agent(ABC):

    def __init__(
        self, 
        name: str,
        tool_registry: ToolRegistry, 
        llm: LLMService,
        skills: list[Skill],
        event_logger: EventLogger
    ):
        self._name = name
        self._tool_registry = tool_registry
        self._llm = llm
        self._skills = skills
        self._event_logger = event_logger

    @abstractmethod
    async def run(self, prompt: str) -> str:
        raise NotImplementedError

    async def execute_llm_request(self, context_item: ContextRoleItem, system_prompt: str, prompt: str) -> LLMResponse:
        await self._log(
            agent=self._name,
            event=EventType.LLM_START,
            query=prompt
        )

        llm_response: LLMResponse = await self._llm.process_beta(
            context_item = context_item, 
            skills = self._skills,
            system_prompt = system_prompt,
            available_tools = self._tool_registry.list_definitions()
        )

        await self._log(
            agent=self._name,
            event=EventType.LLM_END,
            call_id=llm_response.call_id,
            input_tokens = llm_response.usage.input_tokens,
            output_tokens = llm_response.usage.output_tokens
        )
        
        return llm_response

    async def execute_tool(self, tool_name: str, tool_args: str) -> ToolCallResponse:
        await self._log(
            agent=self._name,
            event = EventType.TOOL_START,
            tool_name=tool_name, 
            tool_args=tool_args
        )

        tool_result: ToolCallResponse = await self._tool_registry.execute(
            tool_name=tool_name, 
            tool_args=tool_args
        )

        await self._log(
            agent=self._name,
            event = EventType.TOOL_END,
            tool_name=tool_name,
            tool_result=tool_result.content
        )

        return tool_result

    async def _log(
        self,
        event: EventType,
        agent: str,
        **data: Any
    ) -> None:
        if self._event_logger is None:
            return

        await self._event_logger.log(
            event=event,
            agent=agent,
            **data
        )
