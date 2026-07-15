from .base_tool import Tool
from .tool_definition import ToolDefinition
from ..manager import MCPManager

class RetreiveReceiptDataTool(Tool):
    
    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager):
        super().__init__(definition)
        self._mcp_manager = mcp_manager,
    
    async def execute(self, arguments: dict):
        tool_result = await self._manager.read_resource(
            session_name = "files"
            uri = arguments["uri"]
        )

        return tool_result
