import pytest
from src.game.utils import get_random_tasks, get_impostor_tasks, get_short_tasks, get_long_tasks
from src.game.models.engine import GameLocation
from game.models.tasks import ShortTask, LongTask
from src.game.consts import NUM_SHORT_TASKS, NUM_LONG_TASKS

def test_get_random_tasks_length():
    tasks = get_random_tasks()
    assert len(tasks) == NUM_SHORT_TASKS + NUM_LONG_TASKS

def test_get_random_tasks_types():
    tasks = get_random_tasks()
    assert all([type(task) in (ShortTask, LongTask) for task in tasks])

def test_get_impostor_tasks_length():
    tasks = get_impostor_tasks()
    assert len(tasks) == 1

def test_get_impostor_tasks_type():
    tasks = get_impostor_tasks()
    assert isinstance(tasks[0], ShortTask)

def test_get_impostor_tasks_name():
    tasks = get_impostor_tasks()
    assert tasks[0].name == "Eliminate all crewmates"

def test_get_impostor_tasks_location():
    tasks = get_impostor_tasks()
    assert tasks[0].location == GameLocation.LOC_UNKNOWN

def test_get_short_tasks_length():
    tasks = get_short_tasks()
    assert len(tasks) == NUM_SHORT_TASKS

def test_get_short_tasks_type():
    tasks = get_short_tasks()
    assert all([type(task) == ShortTask for task in tasks])

def test_get_long_tasks_length():
    tasks = get_long_tasks()
    assert len(tasks) == NUM_LONG_TASKS

def test_get_long_tasks_type():
    tasks = get_long_tasks()
    assert all([type(task) == LongTask for task in tasks])
