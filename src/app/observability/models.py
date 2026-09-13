from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

class EventType(str, Enum):
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"

    TASK_START = "task_start"
    TASK_END = "task_end"

    TOOL_START = "tool_start"
    TOOL_END = "tool_end"

    LLM_START = "llm_start"
    LLM_END = "llm_end"

    ERROR = "error"
    