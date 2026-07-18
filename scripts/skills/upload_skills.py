from .skills_service import SkillsService

def create_skill(skill_file_path: str):
    skills_service = SkillsService()

    skills_service.create(skill_file_path)

if __name__ == "__main__":
    create_skill(skill_file_path = "insert-books/SKILL.md")