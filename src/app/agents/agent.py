from abc import ABC, abstractmethod
from typing import Any

from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.llm_response import ToolUse
from src.app.observability.event_logger import EventLogger
from src.app.skills.models import Skill
from src.app.tools.tool_registry import ToolRegistry

class Agent(ABC):

    def __init__(
        self, 
        tool_registry: ToolRegistry, 
        llm: LLMService,
        skills: list[Skill],
        event_logger: EventLogger
    ):
        self._tool_registry = tool_registry
        self._llm = llm
        self._skills = skills
        self._event_logger = event_logger

    @abstractmethod
    async def run(self, prompt: str) -> str:
        raise NotImplementedError

    async def execute_tool(self, tool_call: ToolUse) -> ToolCallResponse:
        tool_result: ToolCallResponse = await self._tool_registry.execute(
            tool_name=tool_call.tool_name, 
            tool_args=tool_call.tool_args
        )
        return tool_result

    async def _log(
        self,
        event: str,
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
        