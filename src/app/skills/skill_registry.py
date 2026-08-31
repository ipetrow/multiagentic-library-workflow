from pathlib import Path
import json

from .models import Skill

SKILLS_FILE_PATH = Path("config/skills.json")

class SkillRegistry:

    def __init__(self):

        with SKILLS_FILE_PATH.open() as f:
            available_skills: list[dict] = json.load(f)["skills"]
            self._skills: dict[str, Skill] = {
                skill_dict["name"]: Skill(**skill_dict)
                for skill_dict in available_skills
            }
                
    def get_skill(self, name: str) -> Skill:
        try: 
            return self._skills[name]
        except KeyError:
            raise ValueError(f"Skill with name {name!r} does not exist!") from None
    
    def has(self, name: str) -> bool:
        return name in self._skills
    
    def get_all(self) -> dict:
        return self._skills
        

    