from pathlib import Path

from src.app.adapters.llm.anthropic_service import AnthropicService
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.mcp.manager import MCPManager
from src.app.agents.analysis_agent import AnalysisAgent
from src.app.agents.library_agent import LibraryAgent
from src.app.skills.skill_registry import SkillRegistry
from src.app.tools.tool_registry_factory import (
    create_library_agent_tool_registry,
    create_analysis_agent_tool_registry
)

async def create_library_agent(
    mcp: MCPManager,
    skill_registry: SkillRegistry,
    analysis_agent: AnalysisAgent
) -> LibraryAgent:

    llm = AnthropicService()

    tool_registry = await create_library_agent_tool_registry(
        mcp_manager = mcp, 
        llm = llm,
        analysis_agent=analysis_agent
    )

    return LibraryAgent(
        tool_registry = tool_registry,
        llm = llm,
        skills=[skill_registry.get_skill(name="insert-books")]
    )

async def create_analysis_agent(
    mcp: MCPManager,
    skill_registry: SkillRegistry
) -> AnalysisAgent:
    
    tool_registry = await create_analysis_agent_tool_registry(mcp_manager=mcp)
    
    return AnalysisAgent(
        tool_registry = tool_registry,
        llm = AnthropicService(),
        skills=[skill_registry.get_skill(name="data-visualization")]
    )
