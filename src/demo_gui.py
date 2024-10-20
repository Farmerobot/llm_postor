import streamlit as st
from game.game_engine import GameEngine
from game.players.ai import AIPlayer
from game.gui_handler import GUIHandler



# To run this script, you need to poetry install and then run the following command:
# streamlit run src/demo_gui.py




def main():
    st.title("Among Us Game - Streamlit")
    gui_handler = GUIHandler()
    game_engine = GameEngine(gui_handler=gui_handler)

    model_name = "gpt-4o-mini"  # Or any other suitable model name

    player_names = ["Wateusz", "Waciej", "Warek"]
    players = [AIPlayer(name=player_names[i], llm_model_name=model_name) for i in range(3)]
    game_engine.load_players(players, impostor_count=1)
    game_engine.init_game()

    try:
        game_engine.enter_main_game_loop()
        st.json(game_engine.to_dict(), expanded=False) # Display final game state
        st.text("\n".join(game_engine.state.playthrough)) # Display final game log

    except Exception as e:
        print(f"Error updating GUI: {e}")
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
