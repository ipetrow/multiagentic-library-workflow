from src.app.api.manager import MCPManager

from .tool_host import (
    RetrieveReceiptDataTool,
    RETRIEVE_RECEIPT_TOOL
)
from .tool_mcp import MCPTool
from .tool_definition import ToolDefinition
from .tool_registry import ToolRegistry

async def register_tools(
        registry: ToolRegistry,
        mcp_manager: MCPManager
) -> ToolRegistry:
    await _register_mcp_tools(registry, mcp_manager)
    _register_host_tools(registry, mcp_manager)

    return registry

async def _register_mcp_tools(registry: ToolRegistry, mcp_manager: MCPManager):

    available_tools: list[dict] = await mcp_manager.get_tools()

    for item in available_tools:
        tool = item["tool"]

        registry.register(
            MCPTool(
                definition = ToolDefinition(
                    name = tool.name,
                    description = tool.description,
                    input_schema = tool.inputSchema
                ), 
                mcp_manager = mcp_manager, 
                session_name = item["session_name"]
            )
        )
    
def _register_host_tools(registry: ToolRegistry, mcp_manager: MCPManager):
    
    registry.register(
        RetrieveReceiptDataTool(
            definition = RETRIEVE_RECEIPT_TOOL, 
            mcp_manager = mcp_manager,
        )
    )