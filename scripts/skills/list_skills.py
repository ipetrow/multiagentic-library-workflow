from .skills_service import SkillsService

def list_all_skills():
    skills_service = SkillsService()

    skills_service.list_all_skills()

if __name__ == "__main__":
    list_all_skills()