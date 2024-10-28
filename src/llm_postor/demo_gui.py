import streamlit as st
from openai import OpenAIError

from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.gui_handler import GUIHandler
from llm_postor.game.models.engine import GamePhase
from llm_postor.game.chat_analyzer import ChatAnalyzer

# To run this script, you need to 
# `poetry install` 
# and then run the following command:
# `poetry run run_gui`

# @st.cache_resource
def load_game_engine():
    game_engine = GameEngine()
    
    # Only for new game. Saved games have llm_model selected in the game state
    model_name = "openai/gpt-4o-mini"
    # model_name = "google/gemini-flash-1.5-exp"
    
    game_engine.init_game()
    if not game_engine.state.players:
        player_names = ["Mateusz", "Andrii", "Vasyl", "Marcin", "Dariusz", "Iwo"]
        players = [
            AIPlayer(name="Mateusz", llm_model_name="gryphe/mythomax-l2-13b"),
            AIPlayer(name="Wojtek", llm_model_name="microsoft/wizardlm-2-8x22b"),
            AIPlayer(name="Lolek", llm_model_name="meta-llama/llama-3.1-8b-instruct"),
            AIPlayer(name="Norbert", llm_model_name="nousresearch/hermes-3-llama-3.1-405b"),
            AIPlayer(name="Nemo", llm_model_name="mistralai/mistral-nemo"),
        ]
        game_engine.load_players(players, impostor_count=1)
    game_engine.state.DEBUG = True
    return game_engine

def main():
    gui_handler = GUIHandler()
    game_engine = load_game_engine()
    chat_analyzer = ChatAnalyzer(players=game_engine.state.players)

    gui_handler.display_gui(game_engine, chat_analyzer)

if __name__ == "__main__":
    main()
