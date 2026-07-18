import os

from anthropic import Anthropic

class SkillsService:

    def __init__(self):
        api_key = os.getenv("AZURE_ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "AZURE_ANTHROPIC_API_KEY environment variable is empty."
            )
        
        self._anthropic = Anthropic(
            api_key=api_key
        )

    def create(self, skill_file_path: str) -> str:
        skill_id = self._anthropic.beta.skills.create(
            files=[
                (
                    skill_file_path,
                    open("skills/{skill_file_path}", "rb"),
                    "text/markdown",
                )
            ]
        )

        print(f"The created skill is with id: {skill_id}")

        return skill_id
    
    def list_all_skills(self):
        skills = self._anthropic.beta.skills.list()

        for skill in skills:
            print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

    def list_custom_skills(self):
        skills = self._anthropic.beta.skills.list(source="custom")

        for skill in skills:
            print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

    def delete_skill(self, skill_id: str):
        # Delete all versions of the Skill
        for version in self._anthropic.beta.skills.versions.list(
            skill_id = skill_id
        ):
            self._anthropic.beta.skills.versions.delete(
                skill_id = skill_id,
                version = version.version
            )

        # Delete the Skill
        self._anthropic.beta.skills.delete(skill_id = skill_id)
    
