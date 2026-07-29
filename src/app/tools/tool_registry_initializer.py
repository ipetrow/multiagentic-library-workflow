from src.app.adapters.mcp.manager import MCPManager
from app.services.retrieve_receipt_books import RetrieveReceiptBooksService
from src.app.adapters.llm.anthropic_service import LLMService

from .definitions.tool_definition import ToolDefinition
from .tool_host import HostTool
from .tool_mcp import MCPTool
from .tool_registry import ToolRegistry
from .definitions.tool_definitions import RETRIEVE_RECEIPT_BOOKS_TOOL

async def register_tools(
        registry: ToolRegistry,
        mcp_manager: MCPManager,
        llm: LLMService
) -> ToolRegistry:
    await _register_mcp_tools(registry, mcp_manager)
    _register_host_tools(registry, mcp_manager, llm)

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
    
def _register_host_tools(registry: ToolRegistry, mcp_manager: MCPManager, llm: LLMService):
    
    registry.register(
        HostTool(
            definition=RETRIEVE_RECEIPT_BOOKS_TOOL,
            handler=RetrieveReceiptBooksService(mcp_manager=mcp_manager, llm=llm)
        )
    )