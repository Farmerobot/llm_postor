from unittest.mock import MagicMock

import pytest
from src.game.players.ai import AIPlayer
from src.game.players.base_player import PlayerRole

@pytest.fixture
def mocked_chat_openai(mocker):
    mocker.patch("src.game.players.ai.ChatOpenAI", return_value=MagicMock())

@pytest.fixture
def mocked_chat_google_generative_ai(mocker):
    mocker.patch("src.game.players.ai.ChatGoogleGenerativeAI", return_value=MagicMock())

@pytest.fixture
def ai_players(mocked_chat_openai, mocked_chat_google_generative_ai):
    player1 = AIPlayer(name="Player 1", llm_model_name="gpt-4o-mini", role=PlayerRole.IMPOSTOR)
    player2 = AIPlayer(name="Player 2", llm_model_name="gpt-4o-mini")
    player3 = AIPlayer(name="Player 3", llm_model_name="gpt-4o-mini")
    return [player1, player2, player3]
