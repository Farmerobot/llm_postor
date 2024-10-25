import os
from dotenv import load_dotenv

# Load environment variables from .env only if not already set
if not os.getenv("OPENAI_API_KEY") or not os.getenv("GOOGLE_GENAI_API_KEY"):
    load_dotenv()

# Retrieve API keys and raise an error if they are missing
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

if not OPENAI_API_KEY and not GOOGLE_GENAI_API_KEY:
    raise ValueError(
        "API keys are missing. Please set OPENAI_API_KEY and/or GOOGLE_GENAI_API_KEY "
        "in your environment or in a .env file."
    )