from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

class ItemType(Enum):
    TOOL = "tool"
    RESOURCE = "resource"

@dataclass(frozen=True)
class ItemKey:
    type: ItemType
    name: str

@dataclass
class ToolCallResponse:
    content: str
    log: str

class Receipt(BaseModel):
    file_name: str
    content: str