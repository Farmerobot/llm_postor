from llm_postor.game.game_engine import GameEngine
from llm_postor.game.gui_handler import GUIHandler
import streamlit as st

# To run this script, you need to 
# `poetry install` 
# and then run the following command:
# `poetry run main`

def main():
    gui_handler = GUIHandler()
    st.set_page_config(page_title="Among Us Game - LLMPostor", layout="wide")
    game_engine = GameEngine()
    
    game_engine.load_game()
    game_engine.state.DEBUG = True
    
    gui_handler.display_gui(game_engine)

if __name__ == "__main__":
    main()
