from typing import Optional, Union
from pydantic import Field, BaseModel, model_validator
from enum import Enum

from game.consts import IMPOSTOR_COOLDOWN
from game.models.game_models import HUMAN_READABLE_LOCATIONS, GameLocation, PlayerState, Task
from game.models.player import Player


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
    player: Player = Field(default_factory=Player)
    target: Optional[Union[Player, GameLocation, Task]] = None
    text: str = ""
    result: str = ""
    spectator: str = ""

    @model_validator(mode='after')
    def set_stories(self):
        if isinstance(self.target, GameLocation):
            self.text = f"move to location {HUMAN_READABLE_LOCATIONS[self.target]}"
            self.result = f"You [{self.player}] moved to {HUMAN_READABLE_LOCATIONS[self.target]}"
            self.spectator = f"{self.player} moved to {HUMAN_READABLE_LOCATIONS[self.target]} from {HUMAN_READABLE_LOCATIONS[self.player.state.location]}"
        elif self.type == GameActionType.WAIT:
            self.text = f"wait in {HUMAN_READABLE_LOCATIONS[self.player.state.location]}"
            self.result = f"You [{self.player}] are waiting in {HUMAN_READABLE_LOCATIONS[self.player.state.location]}"
            self.spectator = f"{self.player} waited"
        elif self.type == GameActionType.DO_ACTION:
            self.text = f"complete task: {self.target.name if isinstance(self.target, Task) else self.target}"
            self.result = f"You [{self.player}] {self.target}"
            self.spectator = f"{self.player} doing task"
        elif self.type == GameActionType.REPORT:
            self.text = f"report dead body of {str(self.target)}"
            self.result = f"You [{self.player}] reported {str(self.target)}"
            self.spectator = f"{self.player} reported dead body of {self.target}"
        elif self.type == GameActionType.KILL:
            self.text = f"eliminate {str(self.target)}"
            self.result = f"You [{self.player}] eliminated {str(self.target)}"
            self.spectator = f"{self.player} eliminated {self.target}"
        elif self.type == GameActionType.VOTE:
            self.text = f"vote for {str(self.target)}"
            self.result = f"You [{self.player}] voted for {str(self.target)}"
            self.spectator = f"{self.player} voted for {self.target}"
        return self

    def do_action(self):
        if (
            self.type == GameActionType.REPORT
            or self.type == GameActionType.WAIT
        ):
            pass
        if self.type == GameActionType.MOVE:
            self.player.state.location = self.target
        if self.type == GameActionType.DO_ACTION:
            return self.target.complete(self.player.state.location)
        if self.type == GameActionType.KILL:
            self.target.state.life = PlayerState.DEAD
            self.player.kill_cooldown = IMPOSTOR_COOLDOWN
        return self.result

    def __str__(self):
        return f"{self.type} | {self.target}"

    def __repr__(self):
        return f"{self.type} | {self.target}"