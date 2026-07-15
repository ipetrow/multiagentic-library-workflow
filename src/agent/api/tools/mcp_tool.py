from .base_tool import Tool
from .tool_definition import ToolDefinition
from ..manager import MCPManager

class MCPTool(Tool):

    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager, session_name: str):
        super().__init__(definition)
        self._mcp_manager = mcp_manager
        self._session_name = session_name

    async def execute(self, arguments):
        tool_result = await self._mcp_manager.call_tool(
            self._definition.name, 
            arguments
        )

        return tool_result