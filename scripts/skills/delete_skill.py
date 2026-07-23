from .skills_service import SkillsService

def delete_skill(skill_id: str):
    skills_service = SkillsService()

    skills_service.delete_skill(skill_id)

if __name__ == "__main__":
    delete_skill("")