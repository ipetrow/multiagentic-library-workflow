from src.app.agents.library_agent import LibraryAgent

class ChatSession:

    def __init__(self, agent: LibraryAgent):
        self._agent = agent

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

                response = await self._agent.run(query)
                print("\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

