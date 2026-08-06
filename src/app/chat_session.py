from src.app.agents.library_agent import LibraryAgent

class ChatSession:

    def __init__(self, agent: LibraryAgent):
        self._agent = agent

    async def run(self):
        """Run an interactive chat session"""

        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self._agent(query)
                print("\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

