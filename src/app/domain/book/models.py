from dataclasses import dataclass, asdict
from enum import Enum

@dataclass
class Book:
    isbn: int | None = None
    title: str
    author: str
    pages_num: int
    reading_status: ReadingStatus

    @classmethod
    def from_dict(cls, book_data: dict) -> Book:
        return cls(**book_data)

    def to_dict(self) -> dict:
        return asdict(self)
    
class ReadingStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    DID_NOT_FINISH = "did_not_finish"