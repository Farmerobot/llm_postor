from enum import Enum
from typing import Optional, Any
from src.game.consts import ASCII_MAP


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


class GameLocation(Enum):
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


HUMAN_READABLE_LOCATIONS = {
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


class Task:
    def __init__(self, name: str, location: GameLocation):
        self.name = name
        self.completed = False
        self.location = location

    def complete(self, location: GameLocation):
        self.completed = True

    def __str__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name}"

    def __repr__(self):
        return f"{'[DONE]' if self.completed else '[TODO]'} | {self.name}"


class ShortTask(Task):
    def __init__(self, name: str, location: GameLocation):
        self.name = name
        self.location = location
        self.completed = False

    def complete(self, location: GameLocation) -> str:
        if self.completed:
            return f"Task {self.name} already completed!"
        if self.location != location:
            return f"Task {self.name} cannot be completed in {HUMAN_READABLE_LOCATIONS[location]}!"
        self.completed = True
        return f"Task {self.name} completed!"


class LongTask(Task):
    def __init__(self, name: str, location: GameLocation):
        self.name = name
        self.location = location
        self.turns_left = 2
        self.completed = False

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
