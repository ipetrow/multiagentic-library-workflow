from abc import ABC, abstractmethod

from .models.models import ContextItem

class LLMService(ABC):

    @abstractmethod
    async def process(self, context_item: ContextItem, system_prompt: str, available_tools: list | None = None) -> str:
        ...