import asyncio

from dotenv import load_dotenv

from src.agent.api.manager import MCPManager
from src.agent.llm.anthropic_service import AnthropicService

async def main():

    load_dotenv()

    llm = AnthropicService()

    async with MCPManager() as mcp:
        try:
            print("List all available tools:")
            llm.list_all_available_skills()

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())