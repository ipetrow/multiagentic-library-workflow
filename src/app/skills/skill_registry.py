from pathlib import Path
import json

from .models import Skill

class SkillRegistry:

    def __init__(self, skill_config_path: Path):

        with skill_config_path.open() as f:
            skills_dict = json.load(f)["skills"]
            self._skills: dict[str, Skill] = {
                skill["name"]: skill
                for skill in skills_dict
            }
                
    def get_skill_id(self, name: str) -> Skill:
        try: 
            return self._skills[name]
        except KeyError:
            raise ValueError(f"Skill with name {name!r} does not exist!") from None
    
    def has(self, name: str) -> bool:
        return name in self._skills
    
    def get_all(self) -> dict:
        return self._skills
        

    