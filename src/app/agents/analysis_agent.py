from src.app.adapters.llm.base_service import LLMService
)
from src.app.skills.skill_registry import SkillRegistry
from src.app.skills.models import Skill
from src.app.tools.tool_registry import ToolRegistry

class AnalysisAgent:

    def __init__(
            self, 
            tool_registry: ToolRegistry, 
            skill_registry: SkillRegistry, 
            llm: LLMService,
            skills: list[Skill]
    ):
        self._tool_registry = tool_registry
        self._skill_registry = skill_registry
        self._llm = llm
        self._skills = skills

    async def run(self, prompt: str) -> str:
        # TODO implement
        pass