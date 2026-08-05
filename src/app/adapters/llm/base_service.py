from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.app.skills.models import Skill

from .models.models import ContextItem

class LLMService(ABC):

    @abstractmethod
    async def process(
        self, 
        context_item: ContextItem, 
        system_prompt: str | None = None, 
        available_tools: list | None = None,
        output_schema: type[BaseModel] | None = None
    ) -> str:
        ...

    @abstractmethod
    async def process_beta(
        self, 
        context_item: ContextItem,
        skills: list[Skill],
        system_prompt: str | None = None, 
        available_tools: list | None = None,
        output_schema: type[BaseModel] | None = None
    ) -> str:
        ...