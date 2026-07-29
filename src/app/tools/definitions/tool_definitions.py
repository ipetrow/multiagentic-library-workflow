from .tool_definition import ToolDefinition

RETRIEVE_RECEIPT_BOOKS_TOOL = ToolDefinition(
    name = "retrieve_receipt_books",
    description = (
        "Retrieve the books from the receipts"
        "Returns: A list of books listed in the receipts pdf files."
    ),
    input_schema = {
        "properties": {},
        "type": "object"
    }
)