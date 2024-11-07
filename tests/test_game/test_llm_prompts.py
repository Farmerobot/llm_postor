import pytest
from llm_postor.game.llm_prompts import (
    ADVENTURE_PLAN_USER_PROMPT,
    ADVENTURE_ACTION_USER_PROMPT,
    DISCUSSION_USER_PROMPT,
    DISCUSSION_RESPONSE_USER_PROMPT,
    VOTING_USER_PROMPT,
    ANNOTATION_SYSTEM_PROMPT,
)

def test_prompt_templates_have_placeholders():
    """
    Check that all prompt templates have placeholders for dynamic content.
    """
    templates = [
        ADVENTURE_PLAN_USER_PROMPT,
        ADVENTURE_ACTION_USER_PROMPT,
        DISCUSSION_USER_PROMPT,
        DISCUSSION_RESPONSE_USER_PROMPT,
        VOTING_USER_PROMPT,
        ANNOTATION_SYSTEM_PROMPT,
    ]
    assert all(template for template in templates)

