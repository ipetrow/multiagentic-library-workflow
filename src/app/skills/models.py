from dataclasses import dataclass

@dataclass(frozen=True)
class Skill:
    name: str
    id: str

    @classmethod
    def from_dict(cls, skill_data: dict) -> Skill:
        return cls(**skill_data)