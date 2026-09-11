import asyncio

from dotenv import load_dotenv

from src.app.adapters.mcp.manager import MCPManager
from src.app.agents.exceptions import MaxStepsExceededError
from src.app.agents.factory import (
    create_library_agent,
    create_analysis_agent
)
from src.app.chat_session import ChatSession
from src.app.config import get_settings
from src.app.observability.event_logger import EventLogger
from src.app.skills.skill_registry import SkillRegistry

async def main():

    load_dotenv()

    event_logger = EventLogger(get_settings().logs_output_dir)

    async with MCPManager() as mcp:
        try:
            skill_registry = SkillRegistry()

            analysis_agent = await create_analysis_agent(
                mcp=mcp, 
                skill_registry=skill_registry,
                event_logger=event_logger
            )

            library_agent = await create_library_agent(
                mcp=mcp, 
                skill_registry=skill_registry,
                analysis_agent=analysis_agent,
                event_logger=event_logger
            )

            try:
                await ChatSession(library_agent).run()
            except MaxStepsExceededError as e:
                print(e)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())
