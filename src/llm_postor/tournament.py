from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.chat_analyzer import ChatAnalyzer

impostor_model = "openai/gpt-4o-mini"
crewmates_model = "meta-llama/llama-3.1-8b-instruct"

players = [
    AIPlayer(name="Mateusz", llm_model_name=impostor_model, role="Impostor"),
    AIPlayer(name="Wojtek", llm_model_name=crewmates_model),
    AIPlayer(name="Lolek", llm_model_name=crewmates_model),
    AIPlayer(name="Norbert", llm_model_name=crewmates_model),
    AIPlayer(name="Nemo", llm_model_name=crewmates_model),
]

game_engine = GameEngine()
game_engine.init_game()
game_engine.state.DEBUG = True
game_engine.load_players(players, impostor_count=1)
chat_analyzer = ChatAnalyzer(players=game_engine.state.players)

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