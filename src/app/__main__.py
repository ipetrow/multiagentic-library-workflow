import asyncio
from pathlib import Path

from dotenv import load_dotenv

from src.app.agents.library_agent import LibraryAgent
from src.app.adapters.mcp.manager import MCPManager
from src.app.tools.tool_registry_initializer import register_tools
from src.app.tools.tool_registry import ToolRegistry
from src.app.adapters.llm.anthropic_service import AnthropicService
from src.app.agents.exceptions import MaxStepsExceededError
from src.app.skills.skill_registry import SkillRegistry

async def main():

    load_dotenv()

    llm = AnthropicService()

    async with MCPManager() as mcp:
        try:
            tools_regsitry = await register_tools(registry = ToolRegistry(), mcp_manager = mcp)

            skills_registry = SkillRegistry(Path("config/skills.json"))

            libAgent = LibraryAgent(
                tool_registry = tools_regsitry,
                skill_registry = skills_registry,
                llm = AnthropicService()
            )

            try:
                libAgent.run()
            except MaxStepsExceededError as e:
                # TODO asks the User for clarification
                print(e)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())