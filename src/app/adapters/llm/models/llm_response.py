from dataclasses import dataclass

@dataclass
class ToolUse:
    tool_name: str
    tool_args: str
    call_id: str

@dataclass
class LLMUsage:
    input_tokens: int
    output_tokens: int

@dataclass
class LLMResponse:
    response: str
    usage: LLMUsage
    tool_use: ToolUse | None = None

    @property
    def is_final(self) -> bool:
        return self.tool_use is None