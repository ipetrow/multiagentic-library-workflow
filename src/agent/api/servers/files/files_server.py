import base64
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .repository import ReceiptRepository

RECEIPTS_DIR = "app/api/servers/files/receipts"
RECEIPTS_FILE = "receipt-001.pdf"

# Initialize FastMCP server
mcp = FastMCP("receipts")

receipts_repository = ReceiptRepository(Path("./receipts/inbox/"))

@mcp.resource("file://receipts/receipt-001.pdf")
def get_receipt_old() -> str:
    """
    Gets the content of a receipt pdf file.

    Returns: the content of the pdf file in a base64 encoded string.   
    """ 

    file_path = os.path.join(RECEIPTS_DIR, RECEIPTS_FILE)
    if os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as pdf_file:
                data = pdf_file.read()
                encoded_file = base64.b64encode(data).decode("utf-8")
        except FileNotFoundError as e:
            print(f"Error reading {file_path}: {str(e)}")
        
        return encoded_file
    
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