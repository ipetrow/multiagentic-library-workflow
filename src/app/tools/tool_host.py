from src.app.adapters.mcp.models.models import ToolCallResponse

from .tool_base import Tool
from .definitions.tool_definition import ToolDefinition
from .tool_handler import Handler

class HostTool(Tool):
    
    def __init__(
            self, 
            definition: ToolDefinition,
            handler: Handler
    ):
        super().__init__(definition),
        self._handler = handler
    
    async def execute(self, arguments: dict) -> ToolCallResponse:
        tool_result = await self._handler.execute(arguments)

        return tool_result
