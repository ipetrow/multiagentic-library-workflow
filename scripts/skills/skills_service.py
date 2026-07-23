import os

from anthropic import AnthropicFoundry

ENDPOINT = "" # TODO add azure endpoint

class SkillsService:

    def __init__(self):
        api_key = os.getenv("AZURE_ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "AZURE_ANTHROPIC_API_KEY environment variable is empty."
            )
        
        self._anthropic = AnthropicFoundry(
            api_key=api_key,
            base_url=ENDPOINT
        )

    def create(self, skill_file_path: str):
        print(f"Creating the skill {skill_file_path}...")

        skill = self._anthropic.beta.skills.create(
            files=[
                (
                    skill_file_path,
                    open(f"skills/{skill_file_path}", "rb"),
                    "text/markdown",
                )
            ]
        )

        print(f"Created the skill {skill_file_path} successfully")

        return skill
    
    def list_all_skills(self):
        print(f"Listing all the skills...")

        try:
            skills = self._anthropic.beta.skills.list()
        except Exception as ex:
            raise ex

        for skill in skills:
            print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

    def list_custom_skills(self):
        print(f"Listing all the custom skills...")

        try:
            skills = self._anthropic.beta.skills.list(source="custom")
        except Exception as ex:
            raise ex

        for skill in skills:
            print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

    def delete_skill(self, skill_id: str):
        print(f"Deleting the skill with id {skill_id}...")

        # Delete all versions of the Skill
        try:
            for version in self._anthropic.beta.skills.versions.list(
                skill_id = skill_id
            ):
                self._anthropic.beta.skills.versions.delete(
                    skill_id = skill_id,
                    version = version.version
                )

            # Delete the Skill
            self._anthropic.beta.skills.delete(skill_id = skill_id)
        except Exception as ex:
            raise ex
        
        print(f"Deleted the skill with id {skill_id} successfully.")