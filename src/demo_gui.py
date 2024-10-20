import streamlit as st
import time
from game.game_engine import GameEngine
from game.players.human import HumanPlayer
from game.players.ai import AIPlayer
from game.players.base_player import PlayerRole

def main():
    st.title("Among Us Game - Streamlit")
    game_engine = GameEngine()

    model_name = "gpt-4o-mini"  # Or any other suitable model name

    player_names = ["Wateusz", "Waciej", "Warek"]
    players = [AIPlayer(name=player_names[i], llm_model_name=model_name) for i in range(3)]
    game_engine.load_players(players, impostor_count=1)
    game_engine.init_game()

    player_states_placeholder = st.empty()
    game_log_placeholder = st.empty()

    try:
        game_engine.enter_main_game_loop()
        while True:
            # player_states = {player.name: player.to_dict() for player in game_engine.state.players}
            game_state = game_engine.to_dict()
            player_states_placeholder.json(game_state, expanded=False)
            game_log_placeholder.text("\n".join(game_engine.state.playthrough))
            time.sleep(0.1)  # Update every 100 milliseconds

    except Exception as e:
        print(f"Error updating GUI: {e}")
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
