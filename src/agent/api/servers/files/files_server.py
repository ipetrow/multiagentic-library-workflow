from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .repository import ReceiptRepository

RECEIPTS_DIR = "src/agent/api/servers/files/receipts/inbox"

# Initialize FastMCP server
mcp = FastMCP("receipts")

receipts_repository = ReceiptRepository(Path(RECEIPTS_DIR))
    
@mcp.resource("receipt://books/inbox")
def get_book_receipts() -> list[dict]:
    """
    Gets the content of a receipt pdf files.

    Returns: the content of the pdf files in a base64 encoded string.   
    """

    return {
        "receipts": receipts_repository.retrieve_receipts() 
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")