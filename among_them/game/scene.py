from __future__ import annotations

import random
import sys
from itertools import chain
from typing import Self

from pydantic import BaseModel, model_validator

from among_them.game.action import MoveAction
from among_them.game.player.base import Player
from among_them.game.tasks import LongTask, ShortTask, Task
from among_them.utils import read_json


class _SceneTask(BaseModel):
    """Model for parsing the task from the location description.

    Attributes:
        text: Text of the task
        turns: Number of turns for a given task to be completed
    """
    text: str
    turns: int | None = 1


class _SceneLocation(BaseModel):
    """Model for parsing the location.

    Attributes:
        name: Name of the location
        doors: Neighboring locations
        tasks: Tasks for a given location
        coordinates: Game coordinates
    """

    name: str
    doors: list[str]
    tasks: list[_SceneTask]
    coordinates: tuple[float, float]


class _Scene(BaseModel):
    """Model for parsing the whole scene.

    Attributes:
        default: Initial location
        locations: Locations of the scene
    """
    default: str
    locations: list[_SceneLocation]

    @model_validator(mode="after")
    def unique_and_doors_exist(self) -> Self:
        location_set = set(self.locations)
        door_set = set(chain(*[loc.doors for loc in _SCENE.locations]))

        not_unique = len(self.locations) != len(location_set)
        door_misalignment = location_set != door_set

        if not_unique or door_misalignment or self.default not in location_set:
            print("Could not validate the scene, quitting...")
            sys.exit(1)
        return self


# Generally, it shouldn't change from game to game
_SCENE = _Scene.model_validate(read_json("configs/scene.json", quit=True))


class Location:
    name: str
    doors: list[Self]
    tasks: list[Task]
    coordinates: tuple[float, float]
    players: list[Player]
    scene: Scene

    def move_actions(self, player: Player) -> list[MoveAction]:
        return [
            MoveAction(
                player=player,
                target=door,
                scene=self.scene
            )
            for door in self.doors
        ]

    def doable_tasks(self, todo_tasks: list[Task]) -> list[Task]:
        doable = {task.name for task in self.tasks}
        return [task for task in todo_tasks if task.name in doable]

    def neighbors(self, player: Player) -> list[Player]:
        return [p for p in self.players if p is not player]


class Scene(BaseModel):
    locations: dict[str, Location]

    def __init__(self, players: list[Player]) -> None:
        # Create locations
        self.locations = {
            scene_location.name: [] for scene_location in _SCENE.locations
        }

        # Fill with players
        self.locations[_SCENE.default].players = [player.name for player in players]

    def _tasks(self) -> tuple[list[ShortTask], list[LongTask]]:
        scene_tasks = list(chain(*[loc.tasks for loc in _SCENE.locations]))
        short_tasks = []
        long_tasks = []
        for scene_task in scene_tasks:
            match scene_task.turns:
                case None:
                    task = ShortTask(name=scene_task.text)
                    short_tasks.append(task)
                case _:
                    task = LongTask(name=scene_task.text, turns_left=scene_task.turns)
                    long_tasks.append(task)
        return short_tasks, long_tasks

    def sample_tasks(
        self, n_short: int, n_long: int
    ) -> tuple[list[ShortTask], list[LongTask]]:
        short_tasks, long_tasks = self._tasks()
        short_tasks = random.sample(short_tasks, n_short)
        long_tasks = random.sample(long_tasks, n_long)
        return short_tasks, long_tasks

    def available_tasks(self, player: Player):
        # tasks in the current location
        # moves
        # eliminations
        pass

    def move(self, player: Player, location: Location):
        current_location = player.state.location
        # assert that neighbors
        # unsubscribe from pverious
        # subscribe to current

    # Subscribe
    def enter(self, player: Player, location: Location):
        assert self.player not in self.mapping[location]
        self.players.append(player)

    # Unsubscribe
    def leave(self, player: Player, location: Location):
        assert player in self.players
        self.players.remove(player)

    def notify(self, message: str):
        # TODO: Kek
        pass

    def dispatch(self, location: str) -> Location:
        ...
