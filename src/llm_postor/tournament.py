from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.chat_analyzer import ChatAnalyzer
from random import shuffle

crewmates_model = "google/gemini-flash-1.5"
impostor_model = "openai/gpt-4o-mini"

players = [
    AIPlayer(name="Mateusz", llm_model_name=impostor_model, role="Impostor"),
    AIPlayer(name="Wojtek", llm_model_name=crewmates_model),
    AIPlayer(name="Lolek", llm_model_name=crewmates_model),
    AIPlayer(name="Norbert", llm_model_name=crewmates_model),
    AIPlayer(name="Nemo", llm_model_name=crewmates_model),
]
shuffle(players)

game_engine = GameEngine()
game_engine.init_game()
game_engine.state.DEBUG = True
game_engine.load_players(players, impostor_count=1)

res = False
while not res:
    try:
        res = game_engine.perform_step()
    except Exception as e:
        if "LLM did" in str(e):
            continue
        else:
            raise e

if game_engine.state.DEBUG: print("Total cost:", game_engine.state.get_total_cost())