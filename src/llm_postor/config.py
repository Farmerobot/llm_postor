import os
from dotenv import load_dotenv

# Load environment variables from .env only if not already set
if not os.getenv("OPENROUTER_API_KEY"):
    load_dotenv()

# Retrieve API keys and raise an error if they are missing
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "API key is missing. Please set OPENROUTER_API_KEY "
        "in your environment or in a .env file in the project root."
    )
    
# if src/llm_postor/game/dummy.py does not exist, create it. This is for abusing streamlit refresh when game_state.json changes
if not os.path.exists("src/llm_postor/game/dummy.py"):
    with open("src/llm_postor/game/dummy.py", "w") as f:
        f.write("timestamp = '2024-11-15 00:20:17.946790'")