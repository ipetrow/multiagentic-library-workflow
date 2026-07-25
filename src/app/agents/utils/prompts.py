from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(finename: str) -> str: 
    prompt_path: Path = PROMPTS_DIR / finename

    return prompt_path.read_text(encoding="utf-8")

