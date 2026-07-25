from src.app.domain.prompt.models import Prompt, PromptType
from src.app.prompts.utils.prompts import load_prompt

from .tool_base import Tool
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

class RetrieveReceiptDataTool(Tool):
    """
    A local host tool that exposes an mcp resource for retrieving the books data in a receipt pdf file.

    Provided to the LLM and based on the User's input, the tool allows the model to dynamicly decide when receipt data is needed.
    """

    SYSTEM_PROMPT = load_prompt(Prompt(type=PromptType.TOOL, filename="retrieve_receipt_data_tool_prompt.md"))
    
    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager):
        super().__init__(definition)
        self._mcp_manager = mcp_manager
    
    async def execute(self, arguments: dict):
        resource = await self._mcp_manager.get_resource(
            session_name = "files",
            resource_uri = "receipt://books/inbox"
            # resource_uri = arguments["uri"]
        )

        # TODO handle the resource

        return resource
