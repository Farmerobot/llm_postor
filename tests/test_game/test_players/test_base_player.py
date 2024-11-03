import copy
from unittest.mock import MagicMock
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.players.base_player import PlayerRole
from llm_postor.game.players.human import HumanPlayer
from llm_postor.game.utils import get_impostor_tasks, get_random_tasks
from llm_postor.game.models.tasks import ShortTask, LongTask
from llm_postor.game.agents.adventure_agent import AdventureAgent
from llm_postor.game.agents.discussion_agent import DiscussionAgent
from llm_postor.game.agents.voting_agent import VotingAgent
from llm_postor.game.models.engine import GameLocation, GamePhase


def create_mock_task(completed=False, location=GameLocation.LOC_CAFETERIA):
    task = MagicMock(spec=ShortTask)
    task.completed = completed
    task.location = location
    return task


def test_role_assignment():
    player = HumanPlayer(name="Test Player", role=PlayerRole.IMPOSTOR)
    player2 = HumanPlayer(name="Test Player 2")
    player2.set_role(PlayerRole.IMPOSTOR)
    assert player.is_impostor is True
    assert player2.is_impostor is True
    assert player.state.tasks == get_impostor_tasks()
    assert player2.state.tasks == get_impostor_tasks()


def test_ai_role_assignment(ai_players):
    player = ai_players[0]
    player2 = ai_players[1]
    player2.set_role(PlayerRole.IMPOSTOR)
    assert player.is_impostor is True
    assert player2.is_impostor is True
    assert player.state.tasks == get_impostor_tasks()
    assert player2.state.tasks == get_impostor_tasks()
    assert player.adventure_agent.role == PlayerRole.IMPOSTOR
    assert player2.adventure_agent.role == PlayerRole.IMPOSTOR
    assert player.discussion_agent.role == PlayerRole.IMPOSTOR
    assert player2.discussion_agent.role == PlayerRole.IMPOSTOR
    assert player.voting_agent.role == PlayerRole.IMPOSTOR
    assert player2.voting_agent.role == PlayerRole.IMPOSTOR


def test_set_stage():
    player = HumanPlayer(name="Test Player")
    player.set_stage(GamePhase.ACTION_PHASE)
    assert player.state.stage == GamePhase.ACTION_PHASE
    assert player.state.location == GameLocation.LOC_CAFETERIA


def test_get_task_to_complete():
    player = HumanPlayer(name="Test Player")
    completed_task = create_mock_task(completed=True)
    incomplete_task = create_mock_task(completed=False)
    player.state.tasks = [completed_task, incomplete_task]
    tasks_to_complete = player.get_task_to_complete()
    assert len(tasks_to_complete) == 1
    assert tasks_to_complete[0] == incomplete_task


def test_log_state_new_round(prev_round_game_stage):
    player = HumanPlayer(name="Test Player")
    player.log_state_new_round(prev_round_game_stage=prev_round_game_stage)
    initial_state = copy.deepcopy(player.state)
    assert player.history.rounds[-1] == initial_state
    assert len(player.state.tasks) == len(get_random_tasks())
    assert player.state.llm_responses == []
    assert player.state.prompt == ""
    assert player.state.actions == []
    assert player.state.response == ""
    assert player.state.action_result == ""
    assert player.state.seen_actions == []
    assert player.state.player_in_room == ""
    assert player.state.observations == []

