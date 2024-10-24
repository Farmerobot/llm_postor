import json
import time
import streamlit as st
from openai import OpenAIError
from types import SimpleNamespace as Namespace

from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.gui_handler import GUIHandler
from llm_postor.game.game_state import GameState
from llm_postor.game.players.fake_ai import FakeAIPlayer
from llm_postor.game.models.engine import GamePhase
from llm_postor.game.chat_analyzer import ChatAnalyzer

# To run this script, you need to poetry install and then run the following command:
# streamlit run src/demo_gui.py

def main():
    st.title("Among Us Game - LLMPostor")
    gui_handler = GUIHandler()
    game_engine = GameEngine()

    model_name = "gpt-4o-mini"  # Or any other suitable model name

    player_names = ["Mateusz", "Andrii", "Vasyl", "Marcin", "Dariusz", "Iwo"]
    try:
        players = [AIPlayer(name=player_names[i], llm_model_name=model_name) for i in range(5)]
        # players = [FakeAIPlayer(name=player_names[i], llm_model_name="fake") for i in range(5)]
        game_engine.load_players(players, impostor_count=1)
    except OpenAIError:
        st.error("OpenAI API key not set")
        return
    
    game_engine.init_game()
    # game_engine.state.set_stage(GamePhase.MAIN_MENU) # pause the game at the main menu
    
    if game_engine.state.game_stage == GamePhase.MAIN_MENU:
        st.warning("Viewing the game state only. No actions are being performed.")
    gui_handler.update_gui(game_engine.state)
    game_engine.state.DEBUG = True

    while not game_engine.perform_step():
        gui_handler.update_gui(game_engine.state)
        # time.sleep(5)
    gui_handler.update_gui(game_engine.state)
    st.text("Game has ended")
    chat_analyzer = ChatAnalyzer(players=game_engine.state.players)
    # chat_analyzer.analyze() returns Dict[str, Dict[str, int]]: with player name as key and dict of persuasive tricks as value with count as value
    # results = chat_analyzer.analyze()
    # st.write(results)
    st.json(game_engine.to_dict(), expanded=False) # Display final game state
    st.text("\n".join(game_engine.state.playthrough)) # Display final game log

if __name__ == "__main__":
    main()
