from base64 import b64encode
import os
from pathlib import Path

class ReceiptRepository:
    
    def __init__(self, path: Path):
        self.path = path

    def list_receipts(self): 
        return self.path.glob("*.pdf")
    
    def retrieve_receipts(self) -> list[dict]:

        receipts = []

        for pdf in self.list_receipts():
            try:
                with open(pdf, "rb") as pdf_file:
                    data = pdf_file.read()
                    file_base64 = b64encode(data).decode("utf-8")

                    receipts.append({
                        "filename": pdf.name,
                        "content": file_base64
                    })
            except FileNotFoundError as e:
                print(f"Error reading {pdf}: {str(e)}")

        return receipts



            


"""
Gets the content of a receipt pdf file.

Returns: the content of the pdf file in a base64 encoded string.   
"""



    
    