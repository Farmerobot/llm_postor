from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union, ForwardRef

from pydantic import BaseModel, model_validator, Field
from game.consts import ASCII_MAP, IMPOSTOR_COOLDOWN

Player = ForwardRef("Player")


class GamePhase(Enum):
    MAIN_MENU = 0
    ACTION_PHASE = 1
    DISCUSS = 2


class PlayerRole(Enum):
    CREWMATE = 0
    IMPOSTOR = 1
    GHOST = 2
    UNKNOWN = 3


class PlayerState(Enum):
    ALIVE = 0
    DEAD = 1
    DEAD_REPORTED = 2


class GameLocation(Enum): # TODO: Replace with string enum with human readable names
    LOC_CAFETERIA = 0
    LOC_REACTOR = 1
    LOC_UPPER_ENGINE = 2
    LOC_LOWER_ENGINE = 3
    LOC_SECURITY = 4
    LOC_MEDBAY = 5
    LOC_ELECTRICAL = 6
    LOC_STORAGE = 7
    LOC_ADMIN = 8
    LOC_COMMUNICATIONS = 9
    LOC_O2 = 10
    LOC_WEAPONS = 11
    LOC_SHIELDS = 12
    LOC_NAVIGATION = 13
    LOC_UNKNOWN = 14


HUMAN_READABLE_LOCATIONS = { # TODO: move to GameLocation enum
    GameLocation.LOC_CAFETERIA: "Cafeteria",
    GameLocation.LOC_REACTOR: "Reactor",
    GameLocation.LOC_UPPER_ENGINE: "Upper Engine",
    GameLocation.LOC_LOWER_ENGINE: "Lower Engine",
    GameLocation.LOC_SECURITY: "Security",
    GameLocation.LOC_MEDBAY: "Medbay",
    GameLocation.LOC_ELECTRICAL: "Electrical",
    GameLocation.LOC_STORAGE: "Storage",
    GameLocation.LOC_ADMIN: "Admin",
    GameLocation.LOC_COMMUNICATIONS: "Communications",
    GameLocation.LOC_O2: "O2",
    GameLocation.LOC_WEAPONS: "Weapons",
    GameLocation.LOC_SHIELDS: "Shields",
    GameLocation.LOC_NAVIGATION: "Navigation",
}

DOORS: dict[GameLocation, list] = {
    GameLocation.LOC_CAFETERIA: [
        GameLocation.LOC_MEDBAY,
        GameLocation.LOC_ADMIN,
        GameLocation.LOC_WEAPONS,
    ],
    GameLocation.LOC_REACTOR: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_LOWER_ENGINE,
    ],
    GameLocation.LOC_UPPER_ENGINE: [
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_MEDBAY,
    ],
    GameLocation.LOC_LOWER_ENGINE: [
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_ELECTRICAL,
    ],
    GameLocation.LOC_SECURITY: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_LOWER_ENGINE,
    ],
    GameLocation.LOC_MEDBAY: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_CAFETERIA,
    ],
    GameLocation.LOC_ELECTRICAL: [
        GameLocation.LOC_LOWER_ENGINE,
        GameLocation.LOC_STORAGE,
    ],
    GameLocation.LOC_STORAGE: [
        GameLocation.LOC_ELECTRICAL,
        GameLocation.LOC_ADMIN,
        GameLocation.LOC_COMMUNICATIONS,
        GameLocation.LOC_SHIELDS,
    ],
    GameLocation.LOC_ADMIN: [GameLocation.LOC_CAFETERIA, GameLocation.LOC_STORAGE],
    GameLocation.LOC_COMMUNICATIONS: [
        GameLocation.LOC_STORAGE,
        GameLocation.LOC_SHIELDS,
    ],
    GameLocation.LOC_O2: [
        GameLocation.LOC_SHIELDS,
        GameLocation.LOC_WEAPONS,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_WEAPONS: [
        GameLocation.LOC_CAFETERIA,
        GameLocation.LOC_O2,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_SHIELDS: [
        GameLocation.LOC_STORAGE,
        GameLocation.LOC_COMMUNICATIONS,
        GameLocation.LOC_O2,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_NAVIGATION: [
        GameLocation.LOC_WEAPONS,
        GameLocation.LOC_O2,
        GameLocation.LOC_SHIELDS,
    ],
}


class GameMap:
    def __init__(self):
        self.map = DOORS

    def get_adjacent(self, location: GameLocation) -> list:
        return self.map[location]

    def __str__(self):
        return ASCII_MAP


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
            return f"Task {self.name} cannot be completed in {HUMAN_READABLE_LOCATIONS[location]}!"
        self.completed = True
        return f"Task {self.name} completed!"

    def __str__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name}"

    def __repr__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name}"


class LongTask(Task):
    turns_left: int = 2
    def complete(self, location: GameLocation) -> str:
        if self.completed:
            return f"Task {self.name} already completed!"
        if self.location != location:
            return f"Task {self.name} cannot be completed in {HUMAN_READABLE_LOCATIONS[location]}!"
        self.turns_left -= 1
        if self.turns_left == 0:
            self.completed = True
            return f"Task {self.name} completed!"
        return f"Task {self.name} requires {self.turns_left} more turns to complete."

    def __str__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name} | {self.turns_left} turns left to finish"

    def __repr__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name} | {self.turns_left} turns left to finish"

class GameActionType(Enum):
    VOTE = -1
    WAIT = 0
    MOVE = 1
    DO_ACTION = 2
    KILL = 3
    REPORT = 4

    def __lt__(self, other):
        if isinstance(other, GameActionType):
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, GameActionType):
            return self.value > other.value
        return NotImplemented


class GameAction(BaseModel):
    type: GameActionType
    source: Player = Field(default_factory=Player)
    target: Optional[Union[Player, GameLocation, Task]] = None
    text: str
    result: str
    spectator: str

    @model_validator(mode='after')
    def set_stories(self):
        if isinstance(self.target, GameLocation):
            self.text = f"move to location {HUMAN_READABLE_LOCATIONS[self.target]}"
            self.result = f"You [{self.source}] moved to {HUMAN_READABLE_LOCATIONS[self.target]}"
            self.spectator = f"{self.source} moved to {HUMAN_READABLE_LOCATIONS[self.target]} from {HUMAN_READABLE_LOCATIONS[self.source.location]}"
        elif self.type == GameActionType.WAIT:
            self.text = f"wait in {HUMAN_READABLE_LOCATIONS[self.source.state.location]}"
            self.result = f"You [{self.source}] are waiting in {HUMAN_READABLE_LOCATIONS[self.source.state.location]}"
            self.spectator = f"{self.source} waited"
        elif self.type == GameActionType.DO_ACTION:
            self.text = f"complete task: {self.target.name if isinstance(self.target, Task) else self.target}"
            self.result = f"You [{self.source}] {self.target}"
            self.spectator = f"{self.source} doing task"
        elif self.type == GameActionType.REPORT:
            self.text = f"report dead body of {str(self.target)}"
            self.result = f"You [{self.source}] reported {str(self.target)}"
            self.spectator = f"{self.source} reported dead body of {self.target}"
        elif self.type == GameActionType.KILL:
            self.text = f"eliminate {str(self.target)}"
            self.result = f"You [{self.source}] eliminated {str(self.target)}"
            self.spectator = f"{self.source} eliminated {self.target}"
        elif self.type == GameActionType.VOTE:
            self.text = f"vote for {str(self.target)}"
            self.result = f"You [{self.source}] voted for {str(self.target)}"
            self.spectator = f"{self.source} voted for {self.target}"
        return self

    def do_action(self):
        if (
            self.type == GameActionType.REPORT
            or self.type == GameActionType.WAIT
        ):
            pass
        if self.type == GameActionType.MOVE:
            self.source.location = self.target
        if self.type == GameActionType.DO_ACTION:
            return self.target.complete(self.source.state.location)
        if self.type == GameActionType.KILL:
            self.target.state.life = PlayerState.DEAD
            self.source.kill_cooldown = IMPOSTOR_COOLDOWN
        return self.result

    def __str__(self):
        return f"{self.type} | {self.target}"

    def __repr__(self):
        return f"{self.type} | {self.target}"
