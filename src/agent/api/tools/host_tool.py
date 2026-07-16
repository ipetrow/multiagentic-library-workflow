from .base_tool import Tool
from .tool_definition import ToolDefinition
from ..manager import MCPManager

RETRIEVE_RECEIPT_TOOL = ToolDefinition(
    name = "retrieve_receipt",
    description = (
        "Retrieve the current book receipts"
        "Returns: A list of the current book receipts pdf files in a base64 encoded strings."
    ),
    input_schema = {
        "properties": {},
        "type": "object"
    }
)

class RetreiveReceiptDataTool(Tool):
    
    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager):
        super().__init__(definition)
        self._mcp_manager = mcp_manager
    
    async def execute(self, arguments: dict):
        tool_result = await self._manager.get_resource(
            session_name = "files",
            resource_uri = arguments["uri"]
        )

        return tool_result
