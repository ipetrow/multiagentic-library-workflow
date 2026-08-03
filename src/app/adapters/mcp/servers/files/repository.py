from base64 import b64encode
from pathlib import Path

class ReceiptRepository:
    
    def __init__(self, receipts_dir: Path):
        self._receipts_dir = receipts_dir
    
    def _find_receipt(self) -> Path:
        receipt = next(self._receipts_dir.glob("*.pdf"), None)

        if receipt is None:
            raise FileNotFoundError(
                f"No receipt found in {self._receipts_dir!r}"
            )

        return receipt

    def retrieve_receipt(self) -> dict:
        receipt = self._find_receipt()

        try:
            with open(receipt, "rb") as pdf_file:
                data = pdf_file.read()
                file_base64 = b64encode(data).decode("utf-8")
        except FileNotFoundError as e:
            print(f"Error reading {pdf_file!r}: {str(e)}")

        return {
            "file_name": receipt.name,
            "content": file_base64
        }  