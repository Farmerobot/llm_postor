import re
from random import sample
from typing import List

from among_them.game import consts
from among_them.game.models.engine import GameLocation
from among_them.game.models.tasks import LongTask, ShortTask, Task


def get_random_tasks() -> list[Task]:
    short_tasks = get_short_tasks()
    long_tasks = get_long_tasks()
    return short_tasks + long_tasks


def get_impostor_tasks() -> list[ShortTask]:
    return [
        ShortTask(name="Eliminate all crewmates", location=GameLocation.LOC_UNKNOWN)
    ]


def get_all_short_tasks() -> list[ShortTask]:
    return [
        ShortTask(
            name="Empty the cafeteria trash", location=GameLocation.LOC_CAFETERIA
        ),
        ShortTask(
            name="Start the coffee maker in the cafeteria",
            location=GameLocation.LOC_CAFETERIA,
        ),
        ShortTask(name="Fix wiring in cafeteria", location=GameLocation.LOC_CAFETERIA),
        ShortTask(
            name="Empty the storage trash chute", location=GameLocation.LOC_STORAGE
        ),
        ShortTask(name="Fix wiring in storage", location=GameLocation.LOC_STORAGE),
        ShortTask(name="Clean the floor in storage", location=GameLocation.LOC_STORAGE),
        ShortTask(
            name="Fix wiring in electrical", location=GameLocation.LOC_ELECTRICAL
        ),
        ShortTask(
            name="Reset breakers in electrical", location=GameLocation.LOC_ELECTRICAL
        ),
        ShortTask(name="Fix wiring in admin", location=GameLocation.LOC_ADMIN),
        ShortTask(name="Clean the floor in admin", location=GameLocation.LOC_ADMIN),
        ShortTask(
            name="Fix wiring in navigation", location=GameLocation.LOC_NAVIGATION
        ),
        ShortTask(
            name="Adjust course in navigation", location=GameLocation.LOC_NAVIGATION
        ),
        ShortTask(
            name="Check headings in navigation", location=GameLocation.LOC_NAVIGATION
        ),
        ShortTask(name="Fix wiring in weapons", location=GameLocation.LOC_WEAPONS),
        ShortTask(
            name="Calibrate targeting system in weapons",
            location=GameLocation.LOC_WEAPONS,
        ),
        ShortTask(name="Fix wiring in shields", location=GameLocation.LOC_SHIELDS),
        ShortTask(name="Fix wiring in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Clean oxygenator filter in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Water plants in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Fix wiring in medbay", location=GameLocation.LOC_MEDBAY),
        ShortTask(
            name="Check catalyzer in upper engine",
            location=GameLocation.LOC_UPPER_ENGINE,
        ),
        ShortTask(
            name="Check catalyzer in lower engine",
            location=GameLocation.LOC_LOWER_ENGINE,
        ),
        ShortTask(
            name="Replace compression coil in upper engine",
            location=GameLocation.LOC_UPPER_ENGINE,
        ),
        ShortTask(
            name="Replace compression coil in lower engine",
            location=GameLocation.LOC_LOWER_ENGINE,
        ),
    ]


def get_short_tasks() -> list[ShortTask]:
    return sample(get_all_short_tasks(), k=consts.NUM_SHORT_TASKS)


def get_short_tasks_by_loc(location: GameLocation) -> list[ShortTask]:
    return [task for task in get_all_short_tasks() if task.location == location]


def get_long_tasks() -> list[LongTask]:
    tasks = [
        LongTask(
            name="Align engine output in upper engine",
            location=GameLocation.LOC_UPPER_ENGINE,
        ),
        LongTask(
            name="Chart course in navigation", location=GameLocation.LOC_NAVIGATION
        ),
        LongTask(name="Clear asteroids in weapons", location=GameLocation.LOC_WEAPONS),
        LongTask(
            name="Route power to defence in electrical",
            location=GameLocation.LOC_ELECTRICAL,
        ),
        LongTask(
            name="Route power to attack in electrical",
            location=GameLocation.LOC_ELECTRICAL,
        ),
        LongTask(name="Prime shields", location=GameLocation.LOC_SHIELDS),
        LongTask(
            name="Process data in communications",
            location=GameLocation.LOC_COMMUNICATIONS,
        ),
        LongTask(name="Run diagnostics in medbay", location=GameLocation.LOC_MEDBAY),
        LongTask(name="Submit scan in medbay", location=GameLocation.LOC_MEDBAY),
    ]
    return sample(tasks, k=consts.NUM_LONG_TASKS)


def check_action_valid(
    available_actions: List[str], chosen_action: str, player_name: str
) -> tuple[int, str]:
    normalized_chosen_action = normalize_action(chosen_action)
    normalized_available_actions = [
        normalize_action(action) for action in available_actions
    ]

    for action in normalized_available_actions:
        if action in normalized_chosen_action:
            return normalized_available_actions.index(action), action

    warning_str = (
        f"{player_name} LLM did not conform to output format. "
        f"Expected one of {normalized_available_actions}, but got '{chosen_action}'"
    )
    print(warning_str)
    raise ValueError(warning_str)


def normalize_action(action: str) -> str:
    return re.sub(r"^\d+[\s:.)-]*", "", action).strip().strip(".").strip("- ").lower()
