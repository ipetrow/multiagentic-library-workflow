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

GENERATE_BAR_CHART_TOOL = ToolDefinition(
    name = "generate_bar_chart",
    description = (
        "Generate a bar chart."
        "Returns: A string containing the generation task status."
    ),
    input_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the bar chart."
            },
            "x_axis_label": {
                "type": "string",
                "description": "The label of the x-axis."
            },
            "y_axis_label": {
                "type": "string",
                "description": "The label of the y-axis."
            },
            "data": {
                "type": "array",
                "description": "The data points to display.",
                "items": {
                    "type": "object",
                    "properties": {
                        "month": {
                            "type": "string",
                            "description": "The category for the y-axis value."
                        },
                        "value": {
                            "type": "string",
                            "description": "The numberic representation of the category for the x-axis value."
                        }
                    },
                    "required": ["month", "value"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["title", "x_axis_label", "y_axis_label", "data"],
        "additionalProperties": False
    }
)
