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
            analysis_agent = create_analysis_agent()

            library_agent = create_library_agent(mcp=mcp, llm=llm, analysis_agent=analysis_agent)

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

    tools_regsitry = await create_library_agent_tool_registry(
        mcp_manager = mcp, 
        llm = llm
    )

    skills_registry = SkillRegistry(Path("config/skills.json"))

    libAgent = LibraryAgent(
        tool_registry = tools_regsitry,
        skill_registry = skills_registry,
        llm = AnthropicService(),
        skills=[skills_registry.get_skill(name="insert-books")]
    )

async def create_analysis_agent() -> AnalysisAgent:
    tools_registry = create_analysis_agent_tool_registry()

    skills_registry = SkillRegistry(Path("config/skills.json"))

    # TODO: 1 - provide correct skill
    
    analysis_agent = AnalysisAgent(
        tool_registry = tools_registry,
        skill_registry = skills_registry,
        llm = AnthropicService(),
        skills=[skills_registry.get_skill(name="insert-books")]
    )

if __name__ == "__main__":
    asyncio.run(main())