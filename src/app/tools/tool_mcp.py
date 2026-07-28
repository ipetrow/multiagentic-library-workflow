from src.app.adapters.mcp.manager import MCPManager
from src.app.adapters.mcp.models.models import ToolCallResponse

from .tool_base import Tool
from .tool_definition import ToolDefinition

class MCPTool(Tool):

    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager, session_name: str):
        super().__init__(definition)
        self._mcp_manager = mcp_manager
        self._session_name = session_name

    async def execute(self, arguments: dict) -> ToolCallResponse: 
        tool_result = await self._mcp_manager.call_tool(
            tool_name = self._definition.name, 
            session_name = self._session_name,
            tool_args = arguments
        )

        return tool_result