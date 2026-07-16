import asyncio

from dotenv import load_dotenv

from src.agent.api.manager import MCPManager
from src.agent.api.tools.tool_registry_initializer import register_tools
from src.agent.api.tools.tool_registry import ToolRegistry
from src.agent.llm.anthropic_service import AnthropicService


async def main():

    load_dotenv()

    llm = AnthropicService()

    async with MCPManager() as mcp:
        try:
            regsitry = await register_tools(registry = ToolRegistry(), mcp_manager = mcp)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())