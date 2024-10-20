from random import randint, sample
from game import consts
from game.models.engine import GameLocation
from game.models.tasks import ShortTask, LongTask


def get_random_tasks() -> list:
    short_tasks = get_short_tasks()
    long_tasks = get_long_tasks()
    return short_tasks + long_tasks


def get_impostor_tasks() -> list:
    return [ShortTask(name="Eliminate all crewmates", location=GameLocation.LOC_UNKNOWN)]


def get_short_tasks() -> list:
    tasks = [
        ShortTask(name="Empty the cafeteria trash", location=GameLocation.LOC_CAFETERIA),
        ShortTask(name="Start the coffee maker in the cafeteria", location=GameLocation.LOC_CAFETERIA),
        ShortTask(name="Fix wiring in cafeteria", location=GameLocation.LOC_CAFETERIA),
        ShortTask(name="Empty the storage trash chute", location=GameLocation.LOC_STORAGE),
        ShortTask(name="Fix wiring in storage", location=GameLocation.LOC_STORAGE),
        ShortTask(name="Clean the floor in storage", location=GameLocation.LOC_STORAGE),
        ShortTask(name="Fix wiring in electrical", location=GameLocation.LOC_ELECTRICAL),
        ShortTask(name="Reset breakers in electrical", location=GameLocation.LOC_ELECTRICAL),
        ShortTask(name="Fix wiring in admin", location=GameLocation.LOC_ADMIN),
        ShortTask(name="Clean the floor in admin", location=GameLocation.LOC_ADMIN),
        ShortTask(name="Fix wiring in navigation", location=GameLocation.LOC_NAVIGATION),
        ShortTask(name="Adjust course in navigation", location=GameLocation.LOC_NAVIGATION),
        ShortTask(name="Check headings in navigation", location=GameLocation.LOC_NAVIGATION),
        ShortTask(name="Fix wiring in weapons", location=GameLocation.LOC_WEAPONS),
        ShortTask(name="Calibrate targeting system in weapons", location=GameLocation.LOC_WEAPONS),
        ShortTask(name="Fix wiring in shields", location=GameLocation.LOC_SHIELDS),
        ShortTask(name="Fix wiring in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Clean oxygenator filter in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Water plants in o2", location=GameLocation.LOC_O2),
        ShortTask(name="Fix wiring in medbay", location=GameLocation.LOC_MEDBAY),
        ShortTask(name="Check catalyzer in upper engine", location=GameLocation.LOC_UPPER_ENGINE),
        ShortTask(name="Check catalyzer in lower engine", location=GameLocation.LOC_LOWER_ENGINE),
        ShortTask(name="Replace compression coil in upper engine", location=GameLocation.LOC_UPPER_ENGINE),
        ShortTask(name="Replace compression coil in lower engine", location=GameLocation.LOC_LOWER_ENGINE),
    ]
    return sample(tasks, k=consts.NUM_SHORT_TASKS)


def get_long_tasks() -> list:
    tasks = [
        LongTask(name="Align engine output in upper engine", location=GameLocation.LOC_UPPER_ENGINE),
        LongTask(name="Chart course in navigation", location=GameLocation.LOC_NAVIGATION),
        LongTask(name="Clear asteroids in weapons", location=GameLocation.LOC_WEAPONS),
        LongTask(name="Route power to defence in electrical", location=GameLocation.LOC_ELECTRICAL),
        LongTask(name="Route power to attack in electrical", location=GameLocation.LOC_ELECTRICAL),
        LongTask(name="Prime shields", location=GameLocation.LOC_SHIELDS),
        LongTask(name="Process data in communications", location=GameLocation.LOC_COMMUNICATIONS),
        LongTask(name="Run diagnostics in medbay", location=GameLocation.LOC_MEDBAY),
        LongTask(name="Submit scan in medbay", location=GameLocation.LOC_MEDBAY),
    ]
    return sample(tasks, k=consts.NUM_LONG_TASKS)
