from abc import ABC, abstractmethod
from itertools import chain
from typing import ClassVar, Self

from pydantic import BaseModel

from among_them.game.action import Action, WaitAction
from among_them.game.player.base import Player
from among_them.game.scene import Scene
from among_them.game.tasks import Task


class Behavior(BaseModel, ABC):
    _behaviors: ClassVar[dict[str, type[Self]]]
    TYPE: ClassVar[str]

    def __init_subclass__(cls) -> None:
        cls._behaviors[cls.TYPE] = cls

    @classmethod
    def dispatch(cls, model: dict) -> Self:
        return cls._behaviors[model["TYPE"]].model_validate(model)

    def __init__(self, scene: Scene) -> None:
        self.tasks = self.initial_tasks(scene)

    @abstractmethod
    def initial_tasks(self, scene: Scene) -> list[Task]:
        ...

    @abstractmethod
    def specific_actions(self, player: Player) -> list[Action]:
        ...

    @abstractmethod
    def perform_callback(self, action: Action) -> None:
        ...

    @abstractmethod
    def available_actions(self, player: Player) -> list[Action]:
        wait_action = [WaitAction(player=player)]
        move_actions = player.location.move_actions(player)
        specific_actions = self.specific_actions(player)
        return list(chain(*[wait_action, move_actions, specific_actions]))
