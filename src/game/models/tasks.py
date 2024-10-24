from abc import ABC, abstractmethod
from pydantic import BaseModel

from game.models.engine import GameLocation


class Task(BaseModel, ABC):
    name: str
    completed: bool = False
    location: GameLocation

    @abstractmethod
    def complete(self, location: GameLocation):
        pass


class ShortTask(Task):
    def complete(self, location: GameLocation) -> str:
        if self.completed:
            return f"Task {self.name} already completed!"
        if self.location != location:
            return f"Task {self.name} cannot be completed in {location.value}!"
        self.completed = True
        return f"Task {self.name} completed!"

    def __str__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name}"


class LongTask(Task):
    turns_left: int = 2

    def complete(self, location: GameLocation) -> str:
        if self.completed:
            return f"Task {self.name} already completed!"
        if self.location != location:
            return f"Task {self.name} cannot be completed in {location.value}!"
        self.turns_left -= 1
        if self.turns_left == 0:
            self.completed = True
            return f"Task {self.name} completed!"
        return f"Task {self.name} requires {self.turns_left} more turns to complete."

    def __str__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name} | {self.turns_left} turns left to finish"
