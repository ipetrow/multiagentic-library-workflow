import json

from pydantic import ValidationError

from src.app.adapters.mcp.manager import MCPManager
from src.app.adapters.mcp.models.models import Receipt
from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.adapters.llm.base_service import LLMService
from src.app.adapters.llm.models.llm_response import LLMResponse
from src.app.adapters.llm.models.models import (
    ContextRoleItem, 
    TextContent, 
    FileContent, 
)
from src.app.schemas.extracted_book import ExtractedBooks
from src.app.domain.prompt.models import Prompt, PromptType
from src.app.prompts.utils.prompts import load_prompt
from src.app.tools.definitions.tool_definitions import RETRIEVE_RECEIPT_BOOKS_TOOL
from src.app.tools.tool_handler import Handler

RESOURCE_NAME = "receipt://books/inbox"
SYSTEM_PROMPT = load_prompt(Prompt(type=PromptType.TOOL, filename="retrieve_receipt_data_tool_sys_prompt.md"))
PROMPT = load_prompt(Prompt(type=PromptType.TOOL, filename="retrieve_receipt_data_tool_prompt.md"))

class RetrieveReceiptBooksService(Handler):
    """
    A local host tool that exposes an mcp resource for retrieving the books data in a receipt pdf file.

    Provided to the LLM and based on the User's input, the tool allows the model to dynamicly decide when receipt data is needed.
    """
    
    def __init__(
            self,
            mcp_manager: MCPManager,
            llm: LLMService
    ):
        self._mcp_manager = mcp_manager
        self._llm = llm
    
    async def execute(self, arguments: dict) -> ToolCallResponse:
        log = f"[Log: Calling tool with name '{RETRIEVE_RECEIPT_BOOKS_TOOL.name}']"

        resource = await self._mcp_manager.get_resource(
            session_name = "files",
            resource_uri = RESOURCE_NAME
        )

        receipt: Receipt = Receipt.model_validate_json(resource)

        context_item = ContextRoleItem(
            role="user",
            content=[
                TextContent(
                    text=PROMPT
                ),
                FileContent(
                    file_name=RESOURCE_NAME,
                    file_data=receipt.content
                )
            ]
        )

        llm_response: LLMResponse = await self._llm.process(
                context_item=context_item, 
                system_prompt=SYSTEM_PROMPT,
                output_schema=ExtractedBooks
            )

        try:
            books = ExtractedBooks.model_validate_json(llm_response.response)

            if not books:
                result = {
                    "valid": "false",
                    "error": "No books were retrieved"
                }

            result = {
                "valid": "true",
                **books.model_dump()
            }
        except ValidationError as error:
            result = {
                "valid": "false",
                "error": str(error)
            }
        
        return ToolCallResponse(content = json.dumps(result), log = log)