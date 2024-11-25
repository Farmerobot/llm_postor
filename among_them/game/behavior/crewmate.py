from itertools import chain
from typing import TYPE_CHECKING, ClassVar, override

from among_them.game.action import Action, TaskAction
from among_them.game.behavior.base import Behavior
from among_them.game.scene import Scene
from among_them.game.tasks import Task

if TYPE_CHECKING:
    from among_them.game.player.base import Player


class Crewmate(Behavior):
    TYPE: ClassVar[str] = "Crewmate"
    n_short_tasks: int
    n_long_tasks: int

    @override
    def initial_tasks(self, scene: Scene) -> list[Task]:
        return list(chain(*scene.sample_tasks(self.n_long_tasks, self.n_long_tasks)))

    @override
    def specific_actions(self, player: Player) -> list[Action]:
        todo = [task for task in player.tasks if task.is_completed]
        return [
            TaskAction(player=player, target=task)
            for task in player.location.doable_tasks(todo)
        ]

    @override
    def perform_callback(self, action: Action) -> None:
        pass
