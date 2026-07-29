from abc import ABC, abstractmethod

from pydantic import BaseModel

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