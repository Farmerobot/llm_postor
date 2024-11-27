import streamlit as st

from among_them.game.game_engine import GameEngine
from among_them.game.gui_handler import GUIHandler

# To run this script, you need to
# `poetry install`
# and then run the following command:
# `poetry run main`


def main():
    gui_handler = GUIHandler()
    st.set_page_config(page_title="Among Them", layout="wide")
    game_engine = GameEngine()

    game_engine.state.DEBUG = True
    game_engine.load_game()

    gui_handler.display_gui(game_engine)


if __name__ == "__main__":
    main()
