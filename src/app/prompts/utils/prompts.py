from pathlib import Path

from src.app.domain.prompt.models import Prompt, PromptType

PROMPTS_DIR = Path(__file__).resolve().parent.parent

def load_prompt(prompt: Prompt) -> str:
    if prompt.type == PromptType.AGENT:
        prompt_path = f"agents/{prompt.filename}"
    elif prompt.type == PromptType.TOOL:
        prompt_path = f"tools/{prompt.filename}"

    prompt_path: Path = PROMPTS_DIR / prompt_path

    return prompt_path.read_text(encoding="utf-8")

