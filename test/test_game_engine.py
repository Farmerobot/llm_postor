import pytest
from src.game.game_engine import GameEngine
from src.game.models.player import Player, PlayerRole


def test_load_players():
    game_engine = GameEngine()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game_engine.load_players([player1, player2])
    assert len(game_engine.players) == 2
    assert player1 in game_engine.players
    assert player2 in game_engine.players


def test_load_players_with_impostor():
    game_engine = GameEngine()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game_engine.load_players([player1, player2], choose_impostor=True)
    assert len(game_engine.players) == 2
    assert sum(1 for p in game_engine.players if p.is_impostor) == 1


def test_load_players_no_impostor():
    game_engine = GameEngine()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game_engine.load_players([player1, player2], choose_impostor=False)
    assert len(game_engine.players) == 2
    assert sum(1 for p in game_engine.players if p.is_impostor) == 0
