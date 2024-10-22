import json
import time
import streamlit as st
from game.game_engine import GameEngine
from game.players.ai import AIPlayer
from game.gui_handler import GUIHandler
from game.game_state import GameState
from types import SimpleNamespace as Namespace
from game.players.fake_ai import FakeAIPlayer



# To run this script, you need to poetry install and then run the following command:
# streamlit run src/demo_gui.py




def main():
    st.title("Among Us Game - Streamlit")
    gui_handler = GUIHandler()
    game_engine = GameEngine(gui_handler=gui_handler)
    game_engine.state.DEBUG = True

    model_name = "gpt-4o-mini"  # Or any other suitable model name

    player_names = ["Wateusz", "Waciej", "Warek", "Wojtek", "Wafał", "Wymek"]
    players = [AIPlayer(name=player_names[i], llm_model_name=model_name) for i in range(5)]
    # players = [FakeAIPlayer(name=player_names[i], llm_model_name="fake") for i in range(6)]
    game_engine.load_players(players, impostor_count=1)
    game_engine.init_game()
    
    # read game_state.json from file
    # with open("game_state.json", "r") as file:
    #     game_state = file.read()
    #     json_game_state = json.loads(game_state, object_hook=lambda d: Namespace(**d))
    #     gui_handler.update_gui(json_game_state)
    #     json_game_state.players[0].state.tasks[0] = "DONE"
    #     gui_handler.update_gui(json_game_state)

    while not game_engine.perform_step():
        gui_handler.update_gui(game_engine.state)
        # time.sleep(5)
    gui_handler.update_gui(game_engine.state)
    st.text("Game has ended")
    st.json(game_engine.to_dict(), expanded=False) # Display final game state
    st.text("\n".join(game_engine.state.playthrough)) # Display final game log


if __name__ == "__main__":
    main()
