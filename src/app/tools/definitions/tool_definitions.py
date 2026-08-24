from .tool_definition import ToolDefinition

RETRIEVE_RECEIPT_BOOKS_TOOL = ToolDefinition(
    name = "retrieve_receipt_books",
    description = (
        "Retrieve the books from the receipt."
        "Returns: A list of books listed in the receipt pdf files."
    ),
    input_schema = {
        "type": "object",
        "properties": {}
    }
)

DELEGATE_ANALYSIS_TOOL = ToolDefinition(
    name = "delegate_analysis",
    description = (
        "Delegate a complex analysis task to an Analysis subagent."
        "Returns: A string containing the analysis task result."
    ),
    input_schema = {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "The analytical task that should be delegated to the analytics subagent."
            }
        },
        "required": ["task"],
        "additionalProperties": False
    }
)