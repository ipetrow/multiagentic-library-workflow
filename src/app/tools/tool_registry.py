import logging

from src.app.adapters.mcp.models.models import ToolCallResponse

from .tool_base import Tool
from .definitions.tool_definition import ToolDefinition 

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
    
    async def get_tool(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError:
            raise ValueError(f"Unknown tool: '{name}'")
    
    async def execute(self, tool_name, tool_args: dict | None = None) -> ToolCallResponse:
        tool = await self.get_tool(tool_name)

        logging.info("Executing %s", tool.definition.name)

        try:
            return await tool.execute(arguments = tool_args or {})
        except Exception as ex:
            logging.exception("Tool with name %s failed", tool.definition.name)
            raise ex