import os
import json
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from llm_postor.config import OPENROUTER_API_KEY
from llm_postor.game.llm_prompts import ANNOTATION_SYSTEM_PROMPT


def annotate_dialogue(dialogue: str, llm_model_name: str = "openai/gpt-4o-mini") -> str:
    """
    Annotates a dialogue with persuasion techniques using OpenAI API.

    Args:
        dialogue: The dialogue to annotate.
        llm_model_name: The OpenAI model to use for annotation.

    Returns:
        The annotated dialogue in the specified format.
    """

    try:
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=llm_model_name,
            temperature=0.1,
        )
        prompt = ANNOTATION_SYSTEM_PROMPT.format()
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=dialogue)
        ])

        # Extract the annotated text from the response
        annotated_text = response.content.strip()
    except Exception as e:
        print(f"Error: {e} while annotating the dialogue: {dialogue}\n", e)
        print("Returning empty string...")
        annotated_text = None

    return annotated_text