import pytest
import random
from src.game.game_engine import GameEngine
from src.game.models.player import Player, PlayerRole, HumanPlayer, AIPlayer


def test_load_human_players():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    game_engine.load_players([player1, player2, player3])
    assert len(game_engine.state.players) == 3
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], HumanPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], HumanPlayer)
    assert game_engine.state.players[2].name == "Player 3"
    assert isinstance(game_engine.state.players[2], HumanPlayer)

def test_load_ai_players():
    game_engine = GameEngine()
    player1 = AIPlayer("Player 1", "gpt-4o-mini")
    player2 = AIPlayer("Player 2", "gpt-4o-mini")
    player3 = AIPlayer("Player 3", "gpt-4o-mini")
    game_engine.load_players([player1, player2, player3])
    assert len(game_engine.state.players) == 3
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], AIPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], AIPlayer)
    assert game_engine.state.players[2].name == "Player 3"
    assert isinstance(game_engine.state.players[2], AIPlayer)


def test_load_human_players_with_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    game_engine.load_players([player1, player2, player3])
    assert len(game_engine.state.players) == 3
    assert sum(1 for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR) == 1


def test_load_human_players_no_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3], impostor_count=0)

def test_load_few_players_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2])

def test_load_imbalanced_team_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    player4 = HumanPlayer("Player 4")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3, player4], impostor_count=2)

def test_load_ten_players_four_impostors():
    game_engine = GameEngine()
    players = [HumanPlayer(f"Player {i}") for i in range(1, 11)]
    game_engine.load_players(players, impostor_count=4)
    assert len(game_engine.state.players) == 10
    assert sum(1 for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR) == 4

def test_one_impostor_when_impostor_count_is_one():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    player4 = HumanPlayer("Player 4", role=PlayerRole.IMPOSTOR)
    game_engine.load_players([player1, player2, player3, player4], impostor_count=1)
    assert sum(1 for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR) == 1
