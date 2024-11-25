from abc import ABC, abstractmethod
from typing import Self

from pydantic import BaseModel


class Task(BaseModel, ABC):
    name: str
    is_completed: bool = False

    def complete(self) -> str:
        if self.is_completed:
            return f"Task {self.name} already completed!"
        return self._complete()

    def _status(self) -> str:
        return "[DONE]" if self.is_completed else "[TODO]"

    @abstractmethod
    def _complete(self) -> str:
        ...


class ShortTask(Task):
    def _complete(self) -> str:
        self.completed = True
        return f"Task {self.name} completed!"

    def __str__(self) -> str:
        return f"{self._status()} | {self.name}"


class LongTask(Task):
    turns_left: int = 2

    def _complete(self) -> str:
        self.turns_left -= 1
        if self.turns_left == 0:
            self.completed = True
            return f"Task {self.name} completed!"

        return f"Task {self.name} requires {self.turns_left} more turns to complete."

    def __str__(self) -> str:
        return f"{self._status()} | {self.name} | {self.turns_left} turns left to finish"
