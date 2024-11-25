from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel

from among_them.game.behavior.impostor import Impostor
from among_them.game.player.base import Player
from among_them.game.scene import Location, Scene
from among_them.game.tasks import Task

if TYPE_CHECKING:
    from among_them.game.engine import Engine


class Action(BaseModel, ABC):
    player: Player

    def perform(self) -> None:
        assert self.player.behavior
        self.player.behavior.perform_callback(self)

    @abstractmethod
    def format_option(self) -> str:
        ...

    @abstractmethod
    def format_message(self) -> str:
        ...

    @abstractmethod
    def format_observe(self) -> str:
        ...


class WaitAction(Action):
    def format_option(self) -> str:
        return f"wait in {self.player.state.location}"

    def format_message(self) -> str:
        return f"You [{self.player}] are waiting in {self.player.state.location}"

    def format_observe(self) -> str:
        return f"{self.player} waited"


class MoveAction(Action):
    target: Location
    scene: Scene

    def perform(self) -> None:
        super().perform()

        assert self.player.state.location != self.target
        self.scene.move(self.player, self.target)

    def format_option(self) -> str:
        return f"move to location {self.target}"

    def format_message(self) -> str:
        return f"You [{self.player}] moved to {self.target}"

    def format_observe(self) -> str:
        return f"{self.player} moved to {self.target} from {self.player.state.location}"


class TaskAction(Action):
    target: Task

    def perform(self) -> None:
        super().perform()

        self.target.complete()

    def format_option(self) -> str:
        return f"complete: {self.target.name}"

    def format_message(self) -> str:
        return f"You [{self.player}] are doing task {self.target.name}"

    def format_observe(self) -> str:
        return f"{self.player} doing task {self.target.name}"


class PretendAction(Action):
    target: Task

    def format_option(self) -> str:
        return f"pretend doing task: {self.target.name}"

    def format_message(self) -> str:
        return f"You [{self.player}] pretended {self.target.name}"

    def format_observe(self) -> str:
        return f"{self.player} are pretending to do {self.target.name}"


class ReportTask(Action):
    target: Player
    engine: Engine

    def perform(self) -> None:
        super().perform()
        assert self.engine.reported is False
        self.engine.reported = True

    def format_option(self) -> str:
        return f"report dead body of {str(self.player)}"

    def format_message(self) -> str:
        return f"You [{self.player}] reported {str(self.target)}"

    def format_observe(self) -> str:
        return f"{self.player} reported dead body of {self.target}"


class KillAction(Action):
    target: Player

    def perform(self) -> None:
        super().perform()
        assert self.player.is_alive
        assert isinstance(self.player.behavior, Impostor)
        assert self.target.is_alive
        self.target.is_alive = False

    def format_option(self) -> str:
        return f"eliminate {str(self.target)}"

    def format_message(self) -> str:
        return f"You [{self.player}] eliminated {str(self.target)}"

    def format_observe(self) -> str:
        return f"{self.player} eliminated {self.target}"


class VoteAction(Action):
    target: Player

    def format_option(self) -> str:
        return f"vote for {str(self.target)}"

    def format_message(self) -> str:
        return f"You [{self.player}] voted for {str(self.target)}"

    def format_observe(self) -> str:
        return f"{self.player} voted for {self.target}"
