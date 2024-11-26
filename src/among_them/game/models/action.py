from enum import IntEnum
from typing import Optional, Self, Union

from pydantic import BaseModel, Field, model_validator

from among_them.game.consts import IMPOSTOR_COOLDOWN
from among_them.game.models.engine import GameLocation
from among_them.game.models.history import PlayerState
from among_them.game.models.tasks import Task
from among_them.game.players.base_player import Player, PlayerRole


class GameActionType(IntEnum):
    VOTE = -1
    WAIT = 0
    MOVE = 1
    DO_ACTION = 2
    KILL = 3
    REPORT = 4
    PRETEND = 5

    def __lt__(self, other: Self):
        if isinstance(other, GameActionType):
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other: Self):
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

    @model_validator(mode="after")
    def set_stories(self):
        if isinstance(self.target, GameLocation):
            self.text = f"move to location {self.target.value}"
            self.result = f"You [{self.player}] moved to {self.target.value}"
            self.spectator = f"{self.player} moved to {self.target.value} from {self.player.state.location.value}"  # noqa: E501
        elif self.type == GameActionType.WAIT:
            self.text = f"wait in {self.player.state.location.value}"
            self.result = (
                f"You [{self.player}] are waiting in {self.player.state.location.value}"
            )
            self.spectator = (
                f"{self.player} waited in {self.player.state.location.value}"
            )
        elif self.type == GameActionType.DO_ACTION:
            self.text = f"complete task: {self.target.name if isinstance(self.target, Task) else self.target}"  # noqa: E501
            self.result = f"You [{self.player}] {self.target}"
            self.spectator = f"{self.player} doing task {self.target.name if isinstance(self.target, Task) else self.target}"  # noqa: E501
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
        elif self.type == GameActionType.PRETEND:
            self.text = f"pretend doing task: {self.target.name if isinstance(self.target, Task) else self.target}"  # noqa: E501
            self.result = f"You [{self.player}] pretended {self.target}"
            self.spectator = f"{self.player} doing task {self.target.name if isinstance(self.target, Task) else self.target}"  # noqa: E501
        return self

    def do_action(self):
        if self.player.role == PlayerRole.IMPOSTOR:
            self.player.kill_cooldown = max(0, self.player.kill_cooldown - 1)
        if self.type in [
            GameActionType.REPORT,
            GameActionType.WAIT,
            GameActionType.PRETEND,
        ]:
            pass
        if self.type == GameActionType.MOVE:
            self.player.state.location = self.target
        if self.type == GameActionType.DO_ACTION:
            return self.target.complete(self.player.state.location)
        if self.type == GameActionType.KILL:
            self.target.state.life = PlayerState.DEAD
            self.player.kill_cooldown = IMPOSTOR_COOLDOWN
            assert isinstance(self.target, Player)
            self.target.state.action_result = f"You were eliminated by {self.player}"
        return self.result

    def __str__(self):
        return f"{self.spectator}"

    def __repr__(self):
        return f"{self.spectator}"
