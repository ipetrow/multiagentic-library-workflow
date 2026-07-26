from abc import ABC, abstractmethod

from src.app.api.models.models import ToolCallResponse

from .tool_definition import ToolDefinition

class Tool(ABC):

    def __init__(self, definition: ToolDefinition):
        self._definition = definition

    @property
    def definition(self) -> ToolDefinition:
        return self._definition

    @abstractmethod
    async def execute(self, arguments: dict) -> ToolCallResponse:
        """Execute the tool with the provided arguments"""
        raise NotImplementedError
