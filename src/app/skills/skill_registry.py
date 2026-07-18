from pathlib import Path
import json

class SkillRegistry:

    def __init__(self, skill_config_path: Path):
        
        with skill_config_path.open() as f:
            self._skills = json.load(f)
    
    def get_skill_id(self, name: str) -> str:
        return self._skills[name]["id"]
    
    def has(self, name: str) -> bool:
        return name in self._skills
    
    def get_all(self) -> dict:
        return self._skills
        

    