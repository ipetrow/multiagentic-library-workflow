from .host_tool import (
    RetreiveReceiptDataTool,
    RETRIEVE_RECEIPT_TOOL
)
from .mcp_tool import MCPTool
from .tool_definition import ToolDefinition
from .tool_registry import ToolRegistry
from ..manager import MCPManager



async def register_tools(
        registry: ToolRegistry,
        mcp_manager: MCPManager
):
    await _register_host_tools(registry, mcp_manager)
    _register_host_tools()

async def _register_mcp_tools(registry: ToolRegistry, mcp_manager: MCPManager):

    available_tools = await mcp_manager.get_tools()

    for tool in available_tools:
        registry.register(
            MCPTool(
                definition = ToolDefinition(
                    name = tool.name,
                    description = tool.description,
                    input_schema = tool.inputSchema
                ), 
                mcp_manager = mcp_manager, 
                session_name = "" # TODO provide the session name
            )
        )
    

def _register_host_tools(registry: ToolRegistry, mcp_manager: MCPManager):
    
    registry.register(
        RetreiveReceiptDataTool(
            definition = RETRIEVE_RECEIPT_TOOL, 
            mcp_manager = mcp_manager,
        )
    )
    