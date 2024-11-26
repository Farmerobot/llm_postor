from typing import Any
from unittest.mock import MagicMock

import pytest

from llm_postor.game.models.engine import GamePhase
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.players.base_player import PlayerRole


@pytest.fixture
def mocked_chat_openai(mocker: Any):
    mocker.patch("llm_postor.game.players.ai.ChatOpenAI", return_value=MagicMock())


@pytest.fixture
def mocked_chat_google_generative_ai(mocker: Any):
    mocker.patch(
        "llm_postor.game.players.ai.ChatGoogleGenerativeAI", return_value=MagicMock()
    )


@pytest.fixture
def ai_players():
    player1 = AIPlayer(
        name="Player 1", llm_model_name="gpt-4o-mini", role=PlayerRole.IMPOSTOR
    )
    player2 = AIPlayer(name="Player 2", llm_model_name="gpt-4o-mini")
    player3 = AIPlayer(name="Player 3", llm_model_name="gpt-4o-mini")
    return [player1, player2, player3]


@pytest.fixture
def prev_round_game_stage():
    return GamePhase.ACTION_PHASE
