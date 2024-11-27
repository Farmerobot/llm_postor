import importlib
import os
from unittest import mock

import pytest

import among_them.config  # Import initially


@pytest.fixture
def clear_env():
    """Clear specific environment variables for testing."""
    with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": ""}):
        yield


def test_missing_openrouter_api_key(clear_env: None):
    # Reload the module to re-evaluate with the cleared environment variable
    with pytest.raises(ValueError, match="API key is missing"):
        importlib.reload(among_them.config)
