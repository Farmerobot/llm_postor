from unittest.mock import MagicMock
from unittest import mock as mocker

def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Mock the AI model agents
    mock_chat_openai = mocker.patch("src.game.players.ai.ChatOpenAI")
    mock_chat_google_ai = mocker.patch("src.game.players.ai.ChatGoogleGenerativeAI")

    # Set the return value for the mocked API call
    mock_chat_openai.return_value = MagicMock()
    mock_chat_google_ai.return_value = MagicMock()


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    

def pytest_unconfigure(config):
    """
    called before test process is exited.
    """