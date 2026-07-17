import asyncio

from dotenv import load_dotenv

from src.app.api.manager import MCPManager
from src.app.api.tools.tool_registry_initializer import register_tools
from src.app.api.tools.tool_registry import ToolRegistry
from src.app.llm.anthropic_service import AnthropicService


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