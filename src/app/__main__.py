import asyncio

from dotenv import load_dotenv

from src.app.agents.library_agent import LibraryAgent
from src.app.api.manager import MCPManager
from src.app.api.tools.tool_registry_initializer import register_tools
from src.app.api.tools.tool_registry import ToolRegistry
from src.app.llm.anthropic_service import AnthropicService
from src.app.agents.exceptions import MaxStepsExceededError



async def main():

    load_dotenv()

    llm = AnthropicService()

    async with MCPManager() as mcp:
        try:
            regsitry = await register_tools(registry = ToolRegistry(), mcp_manager = mcp)

            libAgent = LibraryAgent(tool_registry = regsitry, llm = AnthropicService())

            try:
                libAgent.run()
            except MaxStepsExceededError as e:
                # TODO asks the User for clarification
                print(e)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())