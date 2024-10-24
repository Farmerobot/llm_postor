import pytest
from llm_postor.game.llm_prompts import (
    ADVENTURE_PLAN_TEMPLATE,
    ADVENTURE_ACTION_TEMPLATE,
    DISCUSSION_TEMPLATE,
    DISCUSSION_RESPONSE_TEMPLATE,
    VOTING_TEMPLATE,
    ANNOTATION_TEMPLATE,
    PERSUASION_TECHNIQUES,
)

def test_prompt_templates_have_placeholders():
    """
    Check that all prompt templates have placeholders for dynamic content.
    """
    templates = [
        ADVENTURE_PLAN_TEMPLATE,
        ADVENTURE_ACTION_TEMPLATE,
        DISCUSSION_TEMPLATE,
        DISCUSSION_RESPONSE_TEMPLATE,
        VOTING_TEMPLATE,
        ANNOTATION_TEMPLATE,
        PERSUASION_TECHNIQUES
    ]
    assert all(template for template in templates)

