import streamlit as st
from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field
from streamlit.delta_generator import DeltaGenerator
from annotated_text import annotated_text

from llm_postor.game.game_state import GameState
from llm_postor.game.players.base_player import Player, PlayerRole
from llm_postor.game.models.history import PlayerState
from llm_postor.game.chat_analyzer import ChatAnalyzer

class GUIHandler(BaseModel):
    player_states_placeholders: List[DeltaGenerator] = Field(default_factory=list)
    game_log_placeholder: Optional[DeltaGenerator] = None
    game_log_json: Optional[DeltaGenerator] = None
    cols: List[DeltaGenerator] = Field(default_factory=list)
    model_config = {"arbitrary_types_allowed": True}
    sidebar: List[DeltaGenerator] = Field(default_factory=list)
    
    def init_gui(self, game_state: GameState):
        num_players = len(game_state.players)
        if not self.cols:
            self.cols = [col.empty() for col in st.columns(num_players)]
            for col in self.cols:
                self.player_states_placeholders.append(col.empty())
            # self.player_states_placeholders = [st.empty() for _ in range(num_players)]
        if not self.sidebar:
            sidebar = st.sidebar
            with sidebar:
                for _ in game_state.players:
                    self.sidebar.append(st.empty())
        if not self.game_log_placeholder:
            self.game_log_placeholder = st.empty()
        if not self.game_log_json:
            self.game_log_json = st.empty()
        

    def update_gui(self, game_state: GameState):
        self.init_gui(game_state)
        # for i, (player, col) in enumerate(zip(game_state.players, self.cols)):
        #     with col:
        #         self._display_player_info(player, self.player_states_placeholders[i])
                
        for i, (player, sidebar) in enumerate(zip(game_state.players, self.sidebar)):
            with sidebar:
                self._display_short_player_info(player, st)
        with self.game_log_placeholder.container():
            st.json(game_state.get_total_cost())
            st.text("\n".join(game_state.playthrough))
            annotated_text(
    "[Warek]: I agree that ",
    ("Wateusz's consistent activity in the Cafeteria raises suspicion", "Behavior Analysis"),
    ", while ",
    ("Waciej and Wafał's movement to Medbay should be monitored closely", "Behavior Analysis"),
    ".",
    "[Wojtek]: I saw ",
    ("Wafał eliminate Waciej in Medbay", "Accusation and Finger-Pointing"),
    ", which clearly makes him the impostor we need to vote out.",
    "[Wafał]: I was in Medbay with both Waciej and Wojtek, and I can confirm ",
    ("I did not eliminate anyone", "Alibi Construction"),
    "; we should focus on ",
    ("Wateusz's suspicious activity instead", "Scapegoating"),
    ".",
    "[Wateusz]: I was in the Cafeteria completing tasks and can confirm ",
    ("I did not eliminate Waciej", "Alibi Construction"),
    "; we should focus on verifying ",
    ("Wojtek's claim against Wafał", "Information Manipulation"),
    ".",
    "[Warek]: I suggest we closely examine ",
    ("Wojtek's claim against Wafał", "Information Manipulation"),
    " and gather more details about ",
    ("Wateusz's activities in the Cafeteria", "Behavior Analysis"),
    " before making any decisions.",
    "[Wojtek]: I stand by my claim that ",
    ("Wafał is the impostor for eliminating Waciej", "Accusation and Finger-Pointing"),
    ", and we need to vote him out immediately.",
    "[Wafał]: I was in Medbay with both Waciej and Wojtek, and I did not eliminate anyone; let's focus on ",
    ("Wateusz's suspicious activities in the Cafeteria instead", "Scapegoating"),
    ".",
    "[Wateusz]: I was in the Cafeteria completing tasks and did not eliminate Waciej; we need to clarify ",
    ("Wojtek's claim about Wafał before voting", "Information Manipulation"),
    ".",
    "[Warek]: I believe we should focus on verifying ",
    ("Wojtek's claim about Wafał", "Information Manipulation"),
    " before making any voting decisions.",
    "[Wojtek]: I urge everyone to vote out ",
    ("Wafał immediately based on my eyewitness account", "Confidence Display"),
    " of him eliminating Waciej in Medbay.",
    "[Wafał]: I was in Medbay with both Waciej and Wojtek, and I did not eliminate anyone; we should focus on verifying ",
    ("Wateusz's suspicious activities instead", "Scapegoating"),
    ".",
    "[Wateusz]: I agree that we need to verify ",
    ("Wojtek's claim about Wafał before making any voting decisions", "Information Manipulation"),
    ".",
    "[Warek]: I propose we ask ",
    ("Wojtek for specific details about the elimination", "Information Manipulation"),
    " before making any voting decisions.",
    "[Wojtek]: I stand by my eyewitness account of ",
    ("Wafał eliminating Waciej", "Accusation and Finger-Pointing"),
    " and urge everyone to vote him out immediately.",
    "[Wafał]: I was in Medbay with Waciej and Wojtek, and I didn't eliminate anyone; we should focus on verifying ",
    ("Wateusz's tasks instead", "Scapegoating"),
    ".",
    "[Wateusz]: I agree we need to clarify ",
    ("Wojtek's claim about Wafał before making any voting decisions", "Information Manipulation"),
    ".",
    "[Warek]: ",
    ("Wojtek, please provide specific details about the elimination you witnessed", "Information Manipulation"),
    " to clarify your claim against Wafał.",
    "[Wojtek]: I clearly saw ",
    ("Wafał eliminate Waciej in Medbay", "Accusation and Finger-Pointing"),
    ", and we need to vote him out immediately.",
    "[Wafał]: I agree with investigating ",
    ("Wateusz further", "Scapegoating"),
    ", but let's also press ",
    ("Wojtek for details on his accusation against me", "Information Manipulation"),
    " to clarify the situation."
)
        self.game_log_json.json(game_state.to_dict())
        
    def _display_short_player_info(self, player: Player, placeholder: DeltaGenerator):
        with placeholder.container(border=True): 
            self._display_name_role_status(player)
            self._display_tasks_progress(player)
            with st.expander("Info"):
                self._display_location(player)
                self._display_action_taken(player)
                self._display_action_result(player)
                self._display_recent_actions(player)
                self._display_tasks(player)
        

    def _display_player_info(self, player: Player, placeholder: DeltaGenerator):
        with placeholder.container():  # Clear previous content
            st.subheader(player.name)
            self._display_status(player)
            self._display_role(player)
            self._display_tasks_progress(player)
            self._display_location(player)
            self._display_action_taken(player)
            self._display_action_result(player)
            self._display_recent_actions(player)
            self._display_tasks(player)


    def _display_name_role_status(self, player: Player):
        status_icon = "✅" if player.state.life == PlayerState.ALIVE else "❌"
        role_icon = "😈" if player.role == PlayerRole.IMPOSTOR else "👤"
        complete_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        if player.role == PlayerRole.IMPOSTOR:
            st.write(f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon} ⏳{player.kill_cooldown}")
        else:
            st.write(f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon}")

    def _display_status(self, player: Player):
        status_icon = "✅" if player.state.life == PlayerState.ALIVE else "❌"
        st.write(f"Status: {status_icon} {player.state.life.value}")

    def _display_role(self, player: PlayerRole):
        role_icon = "😈" if player.role == PlayerRole.IMPOSTOR else "👤"
        st.write(f"Role: {role_icon} {player.role.value}")

    def _display_tasks_progress(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.progress(completed_tasks / total_tasks if total_tasks > 0 else 0) #Handle division by zero
        
    def _display_tasks(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.write(f"Tasks: {completed_tasks}/{total_tasks}")
        st.write("Tasks:")
        for task in player.state.tasks:
            st.write(f"- {task}")
        

    def _display_location(self, player: Player):
        st.write(f"Location: {player.state.location.value} {player.state.player_in_room}")
        
    def _display_action_taken(self, player: Player):
        action = player.history.rounds[-1].response
        if action.isdigit():
            st.write(f"Action Taken: {player.history.rounds[-1].actions[int(action)]}")
        else:
            st.write(f"Action Taken: {action}")
        
    def _display_action_result(self, player: Player):
        st.write(f"Action Result: {player.history.rounds[-1].action_result}")

    def _display_recent_actions(self, player: Player):
        st.write("Seen Actions:")
        for action in player.history.rounds[-1].seen_actions:
            st.write(f"- {action}")

