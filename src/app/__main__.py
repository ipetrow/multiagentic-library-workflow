import asyncio
from pathlib import Path

from dotenv import load_dotenv

from src.app.adapters.llm.anthropic_service import AnthropicService
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.mcp.manager import MCPManager
from src.app.agents.analysis_agent import AnalysisAgent
from src.app.agents.exceptions import MaxStepsExceededError
from src.app.agents.library_agent import LibraryAgent
from src.app.chat_session import ChatSession
from src.app.tools.tool_registry_initializer import (
    create_library_agent_tool_registry,
    create_analysis_agent_tool_registry
)

from src.app.skills.skill_registry import SkillRegistry

async def main():

    load_dotenv()

    llm = AnthropicService()

    async with MCPManager() as mcp:
        try:
            analysis_agent = await create_analysis_agent(mcp=mcp)

            library_agent = await create_library_agent(mcp=mcp, llm=llm, analysis_agent=analysis_agent)

            try:   
                await ChatSession(library_agent).run()
            except MaxStepsExceededError as e:
                print(e)

        except Exception as e:
            print(e)

async def create_library_agent(
        mcp: MCPManager,
        llm: LLMService,
        analysis_agent: AnalysisAgent
) -> LibraryAgent:

    tool_registry = await create_library_agent_tool_registry(
        mcp_manager = mcp, 
        llm = llm,
        analysis_agent=analysis_agent
    )

    skills_registry = SkillRegistry(Path("config/skills.json"))

    return LibraryAgent(
        tool_registry = tool_registry,
        skill_registry = skills_registry,
        llm = AnthropicService(),
        skills=[skills_registry.get_skill(name="insert-books")]
    )

async def create_analysis_agent(
        mcp: MCPManager
) -> AnalysisAgent:
    
    tool_registry = await create_analysis_agent_tool_registry(mcp_manager=mcp)

    skills_registry = SkillRegistry(Path("config/skills.json"))

    # TODO: 1 - provide correct skill
    
    return AnalysisAgent(
        tool_registry = tool_registry,
        skill_registry = skills_registry,
        llm = AnthropicService(),
        skills=[skills_registry.get_skill(name="insert-books")]
    )

if __name__ == "__main__":
    asyncio.run(main())