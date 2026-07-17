from .tool_base import Tool
from .tool_definition import ToolDefinition 

class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        name = tool.definition.name

        if name in self._tools:
            raise ValueError(f"Duplicate tool: '{name}'")
        
        self._tools[name] = tool

    def list_definitions(self) -> list[ToolDefinition]:
        return [tool.definition for tool in self._tools.values()]
    
    def get_tool(self, name: str) -> Tool:
        return self._tools[name]
    
    async def execute(self, tool_name, tool_args: dict | None = None):
        tool = self._tools[tool_name]

        return await tool.execute(arguments = tool_args or {})
        