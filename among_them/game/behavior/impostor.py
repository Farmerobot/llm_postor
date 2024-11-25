from typing import ClassVar, override

from among_them.consts import IMPOSTOR_COOLDOWN
from among_them.game.action import Action, KillAction
from among_them.game.behavior.base import Behavior
from among_them.game.player.base import Player
from among_them.game.scene import Scene
from among_them.game.tasks import ShortTask, Task


class Impostor(Behavior):
    NAME: ClassVar[str] = "Impostor"
    kill_cooldown: int = 0

    @override
    def initial_tasks(self, scene: Scene) -> list[Task]:
        return [ShortTask(name="Eliminate all crewmates")]

    @override
    def specific_actions(self, player: Player) -> list[Action]:
        return [
            KillAction(player=player, target=target)
            for target in player.location.neighbors(player)
            if self.kill_cooldown == 0
        ]

    @override
    def perform_callback(self, action: Action) -> None:
        if isinstance(action, KillAction):
            assert self.kill_cooldown == 0
            self.kill_action = IMPOSTOR_COOLDOWN
        else:
            self.kill_action = max(0, self.kill_action - 1)
