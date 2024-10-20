from typing import Any
import streamlit as st
from game.game_state import GameState
from pydantic import BaseModel, Field

class GUIHandler(BaseModel):
    player_states_placeholder: Any = Field(default_factory=st.empty)
    game_log_placeholder: Any = Field(default_factory=st.empty)

    def update_gui(self, game_state: GameState):
        self.player_states_placeholder.json(game_state.to_dict(), expanded=False)
        self.game_log_placeholder.text("\n".join(game_state.playthrough))


