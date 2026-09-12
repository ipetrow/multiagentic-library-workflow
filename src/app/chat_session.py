from src.app.agents.library_agent import LibraryAgent
from src.app.observability.event_logger import EventLogger
from src.app.observability.models import EventType

class ChatSession:

    def __init__(self, agent: LibraryAgent, event_logger: EventLogger):
        self._agent = agent
        self._event_logger = event_logger

    async def run(self):
        """Run an interactive chat session"""

        print("\n\nGuidelines:")
        print("- Type your queries or 'quit' to exit.")
        print("- Use YYYY-MM format for dates. Example: 'Book read in 2026-03'.")
        print("- Generated charts can be found in 'output/charts'.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                await self._event_logger.log(
                    event=EventType.TASK_START
                )

                response = await self._agent.run(query)

                await self._event_logger.log(
                    event=EventType.TASK_END
                )

                print("\n" + response)
            except Exception as e:
                await self._event_logger.log(
                    event=EventType.ERROR,
                    error_type=type(e).__name__,
                    message=str(e)
                )

                print(f"\nError: {str(e)}")

