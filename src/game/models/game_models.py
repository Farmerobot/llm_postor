from enum import Enum
from typing import Optional, Any, Union
from game.consts import ASCII_MAP, IMPOSTOR_COOLDOWN


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


class GameAction:
    from game.models.player import Player 
    def __init__(
        self,
        action: GameActionType,
        source: Player,
        target: Optional[Union[Player, GameLocation, Task, list]] = None,
    ):
        self.action_type: GameActionType = action
        self.source = source
        self.target = target
        self.location = source.get_location()
        self.input_stories = {
            GameActionType.MOVE: f"move to location {HUMAN_READABLE_LOCATIONS[self.target]}" if isinstance(self.target, GameLocation) else "Wait",
            GameActionType.WAIT: f"wait in {HUMAN_READABLE_LOCATIONS[self.location]}",
            GameActionType.DO_ACTION: f"complete task: {self.target.name if isinstance(self.target, Task) else self.target}",
            GameActionType.REPORT: f"report dead body of {str(self.target)}",
            GameActionType.KILL: f"kill {str(self.target)}",
            GameActionType.VOTE: f"vote for {str(self.target)}",
        }
        self.output_stories = {
            GameActionType.MOVE: f"You [{self.source}] moved to {HUMAN_READABLE_LOCATIONS[self.target]}" if isinstance(self.target, GameLocation) else "Wait",
            GameActionType.WAIT: f"You [{self.source}] are waiting in {HUMAN_READABLE_LOCATIONS[self.location]}",
            GameActionType.DO_ACTION: f"You[{self.source}]  {self.target}",
            GameActionType.REPORT: f"You [{self.source}] reported {str(self.target)}",
            GameActionType.KILL: f"You [{self.source}] killed {str(self.target)}",
            GameActionType.VOTE: f"You [{self.source}] voted for {str(self.target)}",
        }
        self.spectator_stories = {
            GameActionType.MOVE: f"{self.source} moved to {HUMAN_READABLE_LOCATIONS[self.target]} from {HUMAN_READABLE_LOCATIONS[self.location]}" if isinstance(self.target, GameLocation) else "Wait",
            GameActionType.WAIT: f"{self.source} waited",
            GameActionType.DO_ACTION: f"{self.source} doing task",
            GameActionType.REPORT: f"{self.source} reported dead body of {self.target}",
            GameActionType.KILL: f"{self.source} killed {self.target}",
            GameActionType.VOTE: f"{self.source} voted for {self.target}",
        }

    def get_input_story(self):
        return self.input_stories[self.action_type]

    def get_output_story(self):
        return self.output_stories[self.action_type]

    def get_spectator_story(self):
        return self.spectator_stories[self.action_type]

    def do_action(self):
        if (
            self.action_type == GameActionType.REPORT
            or self.action_type == GameActionType.WAIT
        ):
            pass
        if self.action_type == GameActionType.MOVE:
            self.source.set_location(self.target)
        if self.action_type == GameActionType.DO_ACTION:
            return self.target.complete(self.target.location)
        if self.action_type == GameActionType.KILL:
            self.target.set_state(PlayerState.DEAD)
            self.source.kill_cooldown = IMPOSTOR_COOLDOWN
        return self.get_output_story()

    def __str__(self):
        return f"{self.action_type} | {self.target}"

    def __repr__(self):
        return f"{self.action_type} | {self.target}"
