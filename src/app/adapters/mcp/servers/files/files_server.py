from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .repository import ReceiptRepository

RECEIPTS_DIR = "src/app/adapters/mcp/servers/files/receipts/inbox"

# Initialize FastMCP server
mcp = FastMCP("receipts")

receipt_repository = ReceiptRepository(Path(RECEIPTS_DIR))
    
@mcp.resource("receipt://books/inbox")
def get_book_receipt() -> dict:
    """
    Gets the content of a receipt pdf file.

    Returns: the content of the pdf file in a base64 encoded string.   
    """

    return receipt_repository.retrieve_receipt()

if __name__ == "__main__":
    mcp.run(transport="stdio")