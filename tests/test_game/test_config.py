import os
import pytest
import importlib
from unittest import mock

import llm_postor.config  # Import initially

@pytest.fixture
def clear_env():
    """Clear specific environment variables for testing."""
    with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": ""}):
        yield

def test_missing_openrouter_api_key(clear_env):
    # Reload the module to re-evaluate with the cleared environment variable
    with pytest.raises(ValueError, match="API key is missing"):
        importlib.reload(llm_postor.config)
