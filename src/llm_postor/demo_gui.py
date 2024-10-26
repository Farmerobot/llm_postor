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
# `poetry run run-gui`

@st.cache_resource
def load_game_engine():
    game_engine = GameEngine()
    
    # Only for new game. Saved games have llm_model selected in the game state
    model_name = "openai/gpt-4o-mini"
    # model_name = "google/gemini-flash-1.5-exp"
    
    game_engine.init_game()
    if not game_engine.state.players:
        player_names = ["Mateusz", "Andrii", "Vasyl", "Marcin", "Dariusz", "Iwo"]
        players = [AIPlayer(name=player_names[i], llm_model_name=model_name) for i in range(5)]
        game_engine.load_players(players, impostor_count=1)
    game_engine.state.DEBUG = True
    return game_engine

def main():
    st.title("Among Us Game - LLMPostor")
    gui_handler = GUIHandler()
    game_engine = load_game_engine()
    make_step = False

    # Create a button to trigger the next step
    if st.button("Make Step"):
        make_step = True

    if make_step:
        game_engine.perform_step()
        make_step = False
        st.rerun()

    gui_handler.display_gui(game_engine.state)
    st.text("Game has ended")
    chat_analyzer = ChatAnalyzer(players=game_engine.state.players)
    # chat_analyzer.analyze() returns Dict[str, Dict[str, int]]: with player name as key and dict of persuasive tricks as value with count as value
    # results = chat_analyzer.analyze()
    # st.write(results)
    st.json(game_engine.state.to_dict(), expanded=False) # Display final game state
    st.text("\n".join(game_engine.state.playthrough)) # Display final game log

if __name__ == "__main__":
    main()
