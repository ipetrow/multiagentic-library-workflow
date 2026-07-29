from abc import ABC, abstractmethod
from typing import Any

class Handler(ABC): 

    @abstractmethod
    async def execute(self, arguments: dict) -> Any:
        """Execute the tool with the provided arguments"""
        raise NotImplementedError