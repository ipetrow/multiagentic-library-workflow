from abc import ABC, abstractmethod

from .tool_definition import ToolDefinition
from ..models.models import ToolCallResponse

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
