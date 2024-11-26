import os

from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from llm_postor.config import OPENROUTER_API_KEY
from llm_postor.game.llm_prompts import ANNOTATION_SYSTEM_PROMPT

# Azure OpenAI credentials - load from environment
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")


def annotate_dialogue(
    dialogue: str, llm_model_name: str = "openai/gpt-4o"
) -> str | None:
    """Annotates a dialogue with persuasion techniques using OpenAI API.

    Args:
        dialogue: The dialogue to annotate.
        llm_model_name: The OpenAI model to use for annotation.

    Returns:
        The annotated dialogue in the specified format.
    """
    try:
        use_azure = False
        # Try to initialize the model
        if use_azure and AZURE_API_KEY and AZURE_ENDPOINT and AZURE_DEPLOYMENT:
            # print(f"Using Azure OpenAI model: {llm_model_name}")
            llm = AzureChatOpenAI(
                openai_api_key=AZURE_API_KEY,
                azure_endpoint=AZURE_ENDPOINT,
                deployment_name=AZURE_DEPLOYMENT,
                model=llm_model_name,
                temperature=0.0,
                api_version="2024-08-01-preview",
            )
        else:
            # Fallback to OpenRouter if Azure credentials are missing
            # or use_azure is False
            # print(f"Using OpenRouter model: {llm_model_name}")
            llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                model=llm_model_name,
                temperature=0.0,
            )
    except Exception as e:
        print(f"Error initializing model {llm_model_name}: {e}")
        return None

    try:
        # Try to invoke the model
        prompt = ANNOTATION_SYSTEM_PROMPT.format()
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=dialogue),
        ])

        # Extract the annotated text from the response
        annotated_text = response.content.strip()
    except Exception as e:
        print(f"Error during model invocation: {e}")
        print(f"Failed to annotate dialogue: {dialogue}\n")
        annotated_text = None

    return annotated_text
