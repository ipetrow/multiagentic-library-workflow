from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel
from mcp.types import Tool

class ItemType(Enum):
    TOOL = "tool"
    RESOURCE = "resource"

@dataclass(frozen=True)
class ItemKey:
    type: ItemType
    name: str

@dataclass(frozen=True)
class ToolCallResponse:
    content: str
    log: str

@dataclass(frozen=True)
class MCPToolEntry:
    session_name: str
    tool: Tool

class Receipt(BaseModel):
    file_name: str
    content: str