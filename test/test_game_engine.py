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
    player2 = HumanPlayer("Player 2", role=PlayerRole.IMPOSTOR) #Adding an impostor before calling load_players
    player3 = HumanPlayer("Player 3")
    game_engine.load_players([player1, player2, player3], choose_impostor=False) #Corrected to choose_impostor=False
    assert len(game_engine.state.players) == 3
    assert sum(1 for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR) == 1


def test_load_human_players_no_impostor_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3], choose_impostor=False)


def test_load_few_players_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2])

def test_load_imbalanced_team_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1", role=PlayerRole.IMPOSTOR)
    player2 = HumanPlayer("Player 2", role=PlayerRole.IMPOSTOR)
    player3 = HumanPlayer("Player 3")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3], choose_impostor=False)


def test_impostor_assignment_randomness():
    game_engine = GameEngine()
    player1 = HumanPlayer("Player 1", role=PlayerRole.IMPOSTOR) #Added an impostor here
    player2 = HumanPlayer("Player 2")
    player3 = HumanPlayer("Player 3")
    impostor_counts = {True: 0, False: 0}
    for _ in range(100):  # Run multiple times to check randomness
        game_engine.load_players([player1, player2, player3], choose_impostor=False) #Corrected to choose_impostor=False
        impostor_counts[game_engine.state.players[0].role == PlayerRole.IMPOSTOR] += 1
        impostor_counts[game_engine.state.players[1].role == PlayerRole.IMPOSTOR] += 1
        impostor_counts[game_engine.state.players[2].role == PlayerRole.IMPOSTOR] += 1

    # Assert that both players have a reasonable chance of being the impostor
    assert impostor_counts[True] > 0
    assert impostor_counts[False] > 0

