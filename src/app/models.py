from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    name: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    is_completed: bool = False
    created_at: Optional[str] = None

    @property
    def display_name(self) -> str:
        return self.name or 'Untitled'


@dataclass
class Tag:
    id: int
    tag_name: str
    description: Optional[str] = None
