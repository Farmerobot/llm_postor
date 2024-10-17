import pytest
from src.game.game_engine import GameEngine
from src.game.models.player import Player, PlayerRole, HumanPlayer, AIPlayer


def test_load_human_players():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    game_engine.load_players([player1, player2])
    assert len(game_engine.state.players) == 2
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], HumanPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], HumanPlayer)

def test_load_ai_players():
    game_engine = GameEngine()
    player1 = AIPlayer("Player 1", "gpt-4o-mini")
    player2 = AIPlayer("Player 2", "gpt-4o-mini")
    game_engine.load_players([player1, player2])
    assert len(game_engine.state.players) == 2
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], AIPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], AIPlayer)


def test_load_human_players_with_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    game_engine.load_players([player1, player2], choose_impostor=True)
    assert len(game_engine.state.players) == 2
    assert sum(1 for player in game_engine.state.players if player.is_impostor) == 1


def test_load_human_players_no_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    game_engine.load_players([player1, player2], choose_impostor=False)
    assert len(game_engine.state.players) == 2
    assert all(not player.is_impostor for player in game_engine.state.players)
