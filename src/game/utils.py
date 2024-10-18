from random import randint, sample
from game import consts
from game.models.game_models import GameLocation, ShortTask, LongTask


def get_random_tasks() -> list:
    short_tasks = get_short_tasks()
    long_tasks = get_long_tasks()
    return short_tasks + long_tasks


def get_short_tasks() -> list:
    tasks = [
        ShortTask("Empty the cafeteria trash", GameLocation.LOC_CAFETERIA),
        ShortTask(
            "Start the coffee maker in the cafeteria", GameLocation.LOC_CAFETERIA
        ),
        ShortTask("Fix wiring in cafeteria", GameLocation.LOC_CAFETERIA),
        ShortTask("Empty the storage trash chute", GameLocation.LOC_STORAGE),
        ShortTask("Fix wiring in storage", GameLocation.LOC_STORAGE),
        ShortTask("Clean the floor in storage", GameLocation.LOC_STORAGE),
        ShortTask("Fix wiring in electrical", GameLocation.LOC_ELECTRICAL),
        ShortTask("Reset breakers in electrical", GameLocation.LOC_ELECTRICAL),
        ShortTask("Fix wiring in admin", GameLocation.LOC_ADMIN),
        ShortTask("Clean the floor in admin", GameLocation.LOC_ADMIN),
        ShortTask("Fix wiring in navigation", GameLocation.LOC_NAVIGATION),
        ShortTask("Adjust course in navigation", GameLocation.LOC_NAVIGATION),
        ShortTask("Check headings in navigation", GameLocation.LOC_NAVIGATION),
        ShortTask("Fix wiring in weapons", GameLocation.LOC_WEAPONS),
        ShortTask("Calibrate targeting system in weapons", GameLocation.LOC_WEAPONS),
        ShortTask("Fix wiring in shields", GameLocation.LOC_SHIELDS),
        ShortTask("Fix wiring in o2", GameLocation.LOC_O2),
        ShortTask("Clean oxygenator filter in o2", GameLocation.LOC_O2),
        ShortTask("Water plants in o2", GameLocation.LOC_O2),
        ShortTask("Fix wiring in medbay", GameLocation.LOC_MEDBAY),
        ShortTask("Check catalyzer in upper engine", GameLocation.LOC_UPPER_ENGINE),
        ShortTask("Check catalyzer in lower engine", GameLocation.LOC_LOWER_ENGINE),
        ShortTask(
            "Replace compression coil in upper engine", GameLocation.LOC_UPPER_ENGINE
        ),
        ShortTask(
            "Replace compression coil in lower engine", GameLocation.LOC_LOWER_ENGINE
        ),
    ]
    return sample(tasks, k=consts.NUM_SHORT_TASKS)


def get_long_tasks() -> list:
    tasks = [
        LongTask("Align engine output in upper engine", GameLocation.LOC_UPPER_ENGINE),
        LongTask("Chart course in navigation", GameLocation.LOC_NAVIGATION),
        LongTask("Clear asteroids in weapons", GameLocation.LOC_WEAPONS),
        LongTask("Route power to defence in electrical", GameLocation.LOC_ELECTRICAL),
        LongTask("Route power to attack in electrical", GameLocation.LOC_ELECTRICAL),
        LongTask("Prime shields", GameLocation.LOC_SHIELDS),
        LongTask("Process data in communications", GameLocation.LOC_COMMUNICATIONS),
        LongTask("Run diagnostics in medbay", GameLocation.LOC_MEDBAY),
        LongTask("Submit scan in medbay", GameLocation.LOC_MEDBAY),
    ]
    return sample(tasks, k=consts.NUM_LONG_TASKS)
