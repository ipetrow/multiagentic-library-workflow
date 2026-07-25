from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class Prompt:
    type: PromptType
    filename: str

class PromptType(Enum):
    AGENT = auto()
    TOOL = auto()