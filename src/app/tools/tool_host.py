import json

from src.app.domain.prompt.models import Prompt, PromptType
from src.app.llm.anthropic_service import AnthropicService
from src.app.llm.models.llm_response import LLMResponse
from src.app.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    FileContent, 
)
from src.app.prompts.utils.prompts import load_prompt


from .tool_base import Tool
from .tool_definition import ToolDefinition
from ..manager import MCPManager
from ..models.models import ToolCallResponse

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

RESOURCE_NAME = "receipt://books/inbox"
SYSTEM_PROMPT = load_prompt(Prompt(type=PromptType.TOOL, filename="retrieve_receipt_data_tool_sys_prompt.md"))
PROMPT = load_prompt(Prompt(type=PromptType.TOOL, filename="retrieve_receipt_data_tool_prompt.md"))

class RetrieveReceiptDataTool(Tool):
    """
    A local host tool that exposes an mcp resource for retrieving the books data in a receipt pdf file.

    Provided to the LLM and based on the User's input, the tool allows the model to dynamicly decide when receipt data is needed.
    """
    
    def __init__(self, definition: ToolDefinition, mcp_manager: MCPManager):
        super().__init__(definition)
        self._mcp_manager = mcp_manager
        self._llm = AnthropicService()
    
    async def execute(self, arguments: dict) -> ToolCallResponse:
        resource = await self._mcp_manager.get_resource(
            session_name = "files",
            resource_uri = RESOURCE_NAME
            # resource_uri = arguments["uri"]
        )

        context_item = ContextRoleItem(
            role="user",
            content=[
                TextContent(
                    text=PROMPT
                ),
                FileContent(
                    file_name=RESOURCE_NAME,
                    file_data=resource
                )
            ]
        )

        books_response: LLMResponse = await self._llm.process(context_item=context_item)
        
        return books_response
