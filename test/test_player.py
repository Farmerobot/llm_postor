from src.game.players.base_player import PlayerRole
from src.game.players.human import HumanPlayer
from src.game.utils import get_impostor_tasks


def test_model_validator_impostor():
    player = HumanPlayer(name="Test Player", role=PlayerRole.IMPOSTOR)
    player2 = HumanPlayer(name="Test Player 2")
    player2.role = PlayerRole.IMPOSTOR
    assert player.is_impostor is True
    assert player2.is_impostor is True
    assert player.state.tasks == get_impostor_tasks()
    assert player2.state.tasks == get_impostor_tasks()