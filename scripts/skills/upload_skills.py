import json
from pathlib import Path

from .skills_service import SkillsService

SKILLS_DIR = Path("skills")
SKILLS_CONFIG_FILE = Path("config/skills.json")

def create_skill(skill_file_path: str) -> str:
    skills_service = SkillsService()

    try:
        skill = skills_service.create(skill_file_path)
    except Exception as ex:
            raise ex
    
    return skill

def add_skills():
    # Deletes the file 
    if SKILLS_CONFIG_FILE.exists():
         print(f"Deleting the file {SKILLS_CONFIG_FILE}")
         SKILLS_CONFIG_FILE.unlink()
         print(f"Deleted the file {SKILLS_CONFIG_FILE} successfully")

    # Collects and creates the available skills
    skills: list[dict[str, str]] = []

    for skill_file in SKILLS_DIR.glob("*/SKILL.md"):
        parent_name = skill_file.parent.name
        file_name = skill_file.name

        skill_path = f"{parent_name}/{file_name}"

        skill = create_skill(skill_file_path = skill_path)
        
        skills.append({
                "name": parent_name,
                "id": skill.id
            })

    data = {
        "skills": skills
    }

    # Recreates the file with the skills
    with SKILLS_CONFIG_FILE.open("w", encoding="utf-8") as file:
         json.dump(data, file, indent=2, ensure_ascii=False)
         file.write("\n")

if __name__ == "__main__":
    add_skills()