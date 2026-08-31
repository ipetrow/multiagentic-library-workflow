from src.app.adapters.mcp.manager import MCPManager
from src.app.adapters.mcp.models.models import MCPToolEntry
from src.app.agents.analysis_agent import AnalysisAgent
from src.app.services.delegate_analysis_service import DelegateAnalysisService
from src.app.services.generate_bar_chart_service import GenerateBarChartService
from src.app.services.retrieve_receipt_books import RetrieveReceiptBooksService
from src.app.adapters.llm.anthropic_service import LLMService

from .definitions.tool_definition import ToolDefinition
from .tool_host import HostTool
from .tool_mcp import MCPTool
from .tool_registry import ToolRegistry
from .definitions.tool_definitions import (
    RETRIEVE_RECEIPT_BOOKS_TOOL,
    DELEGATE_ANALYSIS_TOOL,
    GENERATE_BAR_CHART_TOOL
)

ANALYSIS_MCP_TOOLS = frozenset({
    "get_reading_statistics",
    "generate_bar_chart"
})

LIBRARY_MANAGEMENT_MCP_TOOLS = frozenset({
    "get_all_books",
    "insert_books",
    "update_book_reading_status",
    "update_book_finished_month"
})

async def create_analysis_agent_tool_registry(
        mcp_manager: MCPManager,
) -> ToolRegistry:
    tool_registry = ToolRegistry()

    available_tools: list[MCPToolEntry] = await mcp_manager.get_tools()

    agent_mcp_tools = await _filter_tools(available_tools=available_tools, allowed_tools=ANALYSIS_MCP_TOOLS)

    await _register_mcp_tools(tool_registry, mcp_manager, tools=agent_mcp_tools)

    tool_registry.register(
        HostTool(
            definition=GENERATE_BAR_CHART_TOOL,
            handler=GenerateBarChartService()
        )
    )

    return tool_registry

async def create_library_agent_tool_registry(
        mcp_manager: MCPManager,
        llm: LLMService,
        analysis_agent: AnalysisAgent
) -> ToolRegistry:
    tool_registry = ToolRegistry()

    available_tools: list[MCPToolEntry] = await mcp_manager.get_tools()

    agent_mcp_tools = await _filter_tools(available_tools=available_tools, allowed_tools=LIBRARY_MANAGEMENT_MCP_TOOLS)
    
    await _register_mcp_tools(tool_registry, mcp_manager, tools=agent_mcp_tools)
    await _register_host_tools(tool_registry, mcp_manager, llm)

    tool_registry.register(
        HostTool(
            definition=DELEGATE_ANALYSIS_TOOL,
            handler=DelegateAnalysisService(analysis_agent=analysis_agent)
        )
    )

    return tool_registry

async def _register_mcp_tools(
        registry: ToolRegistry, 
        mcp_manager: MCPManager, 
        tools: list[MCPToolEntry]
):
    for item in tools:
        tool = item.tool

        registry.register(
            MCPTool(
                definition = ToolDefinition(
                    name = tool.name,
                    description = tool.description,
                    input_schema = tool.inputSchema
                ), 
                mcp_manager = mcp_manager, 
                session_name = item.session_name
            )
        )
    
async def _register_host_tools(
        registry: ToolRegistry, 
        mcp_manager: MCPManager, 
        llm: LLMService
):
    
    registry.register(
        HostTool(
            definition=RETRIEVE_RECEIPT_BOOKS_TOOL,
            handler=RetrieveReceiptBooksService(mcp_manager=mcp_manager, llm=llm)
        )
    )

async def _filter_tools(
        available_tools: list[MCPToolEntry], 
        allowed_tools: frozenset
) -> list[MCPToolEntry]:
    return [
        tool_entry
        for tool_entry in available_tools
        if tool_entry.tool.name in allowed_tools
    ]
