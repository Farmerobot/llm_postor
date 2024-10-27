import os
import json
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from llm_postor.config import OPENROUTER_API_KEY
from llm_postor.game.llm_prompts import ANNOTATION_TEMPLATE


def annotate_dialogue(dialogue: str, llm_model_name: str = "openai/gpt-4o-mini") -> str:
    """
    Annotates a dialogue with persuasion techniques using OpenAI API.

    Args:
        dialogue: The dialogue to annotate.
        llm_model_name: The OpenAI model to use for annotation.

    Returns:
        The annotated dialogue in the specified format.
    """

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model=llm_model_name,
        temperature=0.1,
    )
    prompt = ANNOTATION_TEMPLATE.format(dialogue=dialogue)
    response = llm.invoke([HumanMessage(content=prompt)])
    print(response.content)

    # Extract the annotated text from the response
    try:
        annotated_text = response.content.strip()
    except (json.JSONDecodeError, KeyError):
        print("Error parsing response. Returning raw response.")
        return response

    return annotated_text


if __name__ == "__main__":
    # Example usage:
    dialogue = """
    [Warek]: I agree that Wateusz's consistent activity in the Cafeteria raises suspicion, while Waciej and Wafał's movement to Medbay should be monitored closely.
    [Wojtek]: I saw Wafał eliminate Waciej in Medbay, which clearly makes him the impostor we need to vote out.
    [Wafał]: I was in Medbay with both Waciej and Wojtek, and I can confirm I did not eliminate anyone; we should focus on Wateusz's suspicious activity instead.
    [Wateusz]: I was in the Cafeteria completing tasks and can confirm I did not eliminate Waciej; we should focus on verifying Wojtek's claim against Wafał.
    [Warek]: I suggest we closely examine Wojtek's claim against Wafał and gather more details about Wateusz's activities in the Cafeteria before making any decisions.
    [Wojtek]: I stand by my claim that Wafał is the impostor for eliminating Waciej, and we need to vote him out immediately.
    [Wafał]: I was in Medbay with both Waciej and Wojtek, and I did not eliminate anyone; let's focus on Wateusz's suspicious activities in the Cafeteria instead.
    [Wateusz]: I was in the Cafeteria completing tasks and did not eliminate Waciej; we need to clarify Wojtek's claim about Wafał before voting.
    [Warek]: I believe we should focus on verifying Wojtek's claim about Wafał before making any voting decisions.
    [Wojtek]: I urge everyone to vote out Wafał immediately based on my eyewitness account of him eliminating Waciej in Medbay.
    [Wafał]: I was in Medbay with both Waciej and Wojtek, and I did not eliminate anyone; we should focus on verifying Wateusz's suspicious activities instead.
    [Wateusz]: I agree that we need to verify Wojtek's claim about Wafał before making any voting decisions.
    [Warek]: I propose we ask Wojtek for specific details about the elimination before making any voting decisions.
    [Wojtek]: I stand by my eyewitness account of Wafał eliminating Waciej and urge everyone to vote him out immediately.
    [Wafał]: I was in Medbay with Waciej and Wojtek, and I didn't eliminate anyone; we should focus on verifying Wateusz's tasks instead.
    [Wateusz]: I agree we need to clarify Wojtek's claim about Wafał before making any voting decisions.
    [Warek]: Wojtek, please provide specific details about the elimination you witnessed to clarify your claim against Wafał.
    [Wojtek]: I clearly saw Wafał eliminate Waciej in Medbay, and we need to vote him out immediately.
    [Wafał]: I agree with investigating Wateusz further, but let's also press Wojtek for details on his accusation against me to clarify the situation.
    """
    annotated_dialogue = annotate_dialogue(dialogue)
    print(annotated_dialogue)
