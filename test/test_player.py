from src.game.players.ai import AIPlayer
from src.game.players.base_player import PlayerRole
from src.game.players.human import HumanPlayer
from src.game.utils import get_impostor_tasks


def test_role_assignment():
    player = HumanPlayer(name="Test Player", role=PlayerRole.IMPOSTOR)
    player2 = HumanPlayer(name="Test Player 2")
    player2.set_role(PlayerRole.IMPOSTOR)
    assert player.is_impostor is True
    assert player2.is_impostor is True
    assert player.state.tasks == get_impostor_tasks()
    assert player2.state.tasks == get_impostor_tasks()
    
def test_ai_role_assignment():
    player = AIPlayer(name="Test Player", llm_model_name="gpt-4o-mini", role=PlayerRole.IMPOSTOR)
    player2 = AIPlayer(name="Test Player 2", llm_model_name="gpt-4o-mini")
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