from src.app.adapters.mcp.models.models import ToolCallResponse

from .tool_base import Tool
from .definitions.tool_definition import ToolDefinition
from .tool_handler import Handler

class HostTool(Tool):
    """
    A local host tool that exposes an mcp resource for retrieving the books data in a receipt pdf file.

    Provided to the LLM and based on the User's input, the tool allows the model to dynamicly decide when receipt data is needed.
    """
    
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


