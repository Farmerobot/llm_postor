import json
import random
import uuid
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import streamlit as st
from collections import defaultdict, Counter
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from streamlit.delta_generator import DeltaGenerator
from annotated_text import annotated_text
from llm_postor.annotation import annotate_dialogue
from llm_postor.game.game_state import GameState
from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.base_player import Player, PlayerRole
from llm_postor.game.models.history import PlayerState, RoundData
from llm_postor.game.models.engine import ROOM_COORDINATES
import plotly.graph_objects as go
from llm_postor.game.chat_analyzer import ChatAnalyzer


class GUIHandler(BaseModel):
    def display_gui(self, game_engine: GameEngine):
        st.set_page_config(page_title="Among Us Game - LLMPostor", layout="wide")
        game_overwiew, tournements = st.tabs(["Game Overview", "Tournaments"])
        with game_overwiew:
            self.game_overview(game_engine)
        with tournements:
            self.tournements()
        with st.sidebar:
            with st.container():
                st.write(f"{game_engine.state.game_stage.value}. Total cost: {round(game_engine.state.get_total_cost()['total_cost'], 3)}$")
            for i, player in enumerate(game_engine.state.players):
                with st.empty():
                    self._display_short_player_info(
                        player, i == game_engine.state.player_to_act_next, st
                    )

    def game_overview(self, game_engine: GameEngine):
        st.title("Among Us Game - LLMPostor")
        # Create a button to trigger the next step
        should_perform_step = st.button("Make Step")
        col1, col2 = st.columns([2,1])
        with col1:
            self._display_map(game_engine.state)
        with col2:
            with st.container(height=300):
                st.text("\n".join(game_engine.state.playthrough))
        self._display_player_selection(game_engine.state.players)
        discussion = self._display_discussion_chat(game_engine.state.players)
        # Analyze Chat Button
        if st.button("Analyze Chat"):
            # results = chat_analyzer.analyze()
            results = annotate_dialogue(discussion)
            st.session_state.results = results
        if "results" in st.session_state:
            self._display_annotated_text(json.loads(st.session_state.results), game_engine.state.players)
        # Cost Visualization
        cost_data = self.get_cost_data(game_engine)
        if game_engine.state.round_number >= 1:
            estimated_cost_data = self.estimate_future_cost(cost_data, 5)
            combined_cost_data = self.combine_data(cost_data, estimated_cost_data)
            self.plot_cost(combined_cost_data, 5)
        
        if st.session_state.selected_player < len(game_engine.state.players):
            player: Player = game_engine.state.players[st.session_state.selected_player]
            st.subheader(f"Player: {player.name} Chat History:")
            self._display_chat_history(player.history.rounds)
        
        st.text("Cost Breakdown:")
        st.json(game_engine.state.get_total_cost(), expanded=False)
        st.text("Raw Game State:")
        st.json(game_engine.state.to_dict(), expanded=False)
            
        if should_perform_step:
            print("Performing step")
            game_engine.perform_step()
            st.rerun()

    import os

    def tournaments(self):
        st.write("This is the Tournaments tab. Content will be added here.")
        
        # Directory containing tournament JSON files
        tournament_dir = "data/tournament"
        
        # List all JSON files in the directory
        tournament_files = [f for f in os.listdir(tournament_dir) if f.endswith('.json')]
        
        # Iterate over each file and load the game state
        for file_name in tournament_files:
            file_path = os.path.join(tournament_dir, file_name)
            
            # Create a new GameEngine instance
            game_engine = GameEngine()
            
            # Load the game state from the file
            if game_engine.load_state(file_path):
                st.subheader(f"Tournament: {file_name}")
                st.write(f"Game Stage: {game_engine.state.game_stage}")
                st.write(f"Number of Players: {len(game_engine.state.players)}")
                st.write(f"Round Number: {game_engine.state.round_number}")
                # Add more details as needed
            else:
                st.write(f"Failed to load tournament from {file_name}")

    def _display_short_player_info(
        self, player: Player, current: bool, placeholder: DeltaGenerator
    ):
        with placeholder.container(border=True):
            self._display_name_role_status(player, current)
            self._display_tasks_progress(player)
            with st.expander("Info"):
                self._display_location(player)
                self._display_action_taken(player)
                self._display_action_result(player)
                self._display_recent_actions(player)
                self._display_tasks(player)

    def _display_name_role_status(self, player: Player, current: bool):
        status_icon = "✅" if player.state.life == PlayerState.ALIVE else "❌"
        role_icon = "😈" if player.role == PlayerRole.IMPOSTOR else "👤"
        current_icon = "⭐️" if current else ""
        complete_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        if player.role == PlayerRole.IMPOSTOR:
            st.write(
                f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon} ⏳{player.kill_cooldown} {current_icon}"
            )
        else:
            st.write(
                f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon} {current_icon}"
            )

    def _display_tasks_progress(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.progress(
            completed_tasks / total_tasks if total_tasks > 0 else 0
        )  # Handle division by zero

    def _display_tasks(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.write(f"Tasks: {completed_tasks}/{total_tasks}")
        st.write("Tasks:")
        for task in player.state.tasks:
            st.write(f"- {task}")

    def _display_location(self, player: Player):
        st.write(
            f"Location: {player.state.location.value} {player.state.player_in_room}"
        )

    def _display_action_taken(self, player: Player):
        action = player.state.response
        if action.isdigit():
            st.write(f"Action Taken: {player.state.actions[int(action)]}")
        else:
            st.write(f"Action Taken: {action}")

    def _display_action_result(self, player: Player):
        st.write(f"Action Result: {player.state.action_result}")

    def _display_recent_actions(self, player: Player):
        st.write("Seen Actions:")
        for action in player.state.seen_actions:
            st.write(f"- {action}")

    def _display_map(self, game_state: GameState):
        fig = go.Figure()
        img_width = 836
        img_height = 470
        scale_factor = 0.5

        # Add invisible scatter trace.
        # This trace is added to help the autoresize logic work.
        fig.add_trace(
            go.Scatter(
                x=[0, img_width * scale_factor],
                y=[0, img_height * scale_factor],
                mode="markers",
                marker_opacity=0,
            )
        )

        # Configure axes
        fig.update_xaxes(visible=False, range=[0, img_width * scale_factor])
        fig.update_yaxes(
            visible=False,
            range=[0, img_height * scale_factor],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x",
        )

        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source="https://d.techtimes.com/en/full/374414/electrical.png?w=836&f=111ca30545788b099bf5224400a2dbca",
            )
        )

        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        # Add player markers
        def update_player_markers(game_state: GameState):
            fig.data = []  # Clear existing traces
            for i, player in enumerate(game_state.players):
                x, y = ROOM_COORDINATES[player.state.location]
                marker_color = "yellow" if player.role == PlayerRole.CREWMATE else "red"
                marker_size = 15
                marker_symbol = (
                    "circle" if player.role == PlayerRole.CREWMATE else "square"
                )

                # Highlight the player to act next
                if i == game_state.player_to_act_next:
                    marker_size = 25
                    marker_symbol = "star"

                fig.add_trace(
                    go.Scatter(
                        x=[x * 100 + random.randint(-10, 10)],
                        y=[y * 100 + random.randint(-10, 10)],
                        mode="markers",
                        marker=dict(
                            color=marker_color,
                            size=marker_size,
                            symbol=marker_symbol,
                        ),
                        name=player.name,
                        customdata=[
                            f"<b>{player.name}</b><br>Role: {player.role.value}<br>Status: {player.state.life.value}"
                        ],
                        hovertemplate="%{customdata}",
                    )
                )

        update_player_markers(game_state)

        # Display the map
        map_placeholder = st.empty()
        map_placeholder.plotly_chart(fig, use_container_width=True, key=uuid.uuid4())

    def _display_annotated_text(self, json_data: List[dict], players: List[Player]):
        args = []
        previous_player = None
        player_techniques = defaultdict(list)
        
        for item in json_data:
            replaced_text = item["text"]
            current_player = replaced_text.split("]:")[0].strip("[]") if "]: " in replaced_text else previous_player

            if previous_player and previous_player != current_player:
                args.append("\n\n")

            if item["annotation"]:
                combined_annotation = ", ".join(item["annotation"])
                args.append((replaced_text, combined_annotation))
                player_techniques[current_player].extend(item["annotation"])
            else:
                args.append(replaced_text)

            previous_player = current_player

        annotated_text(*args)

        # Determine unique models used by each team
        crewmates = [p for p in players if not p.is_impostor]
        impostors = [p for p in players if p.is_impostor]
        
        crewmate_models = set(p.llm_model_name for p in crewmates)
        impostor_models = set(p.llm_model_name for p in impostors)

        # Flag to check if only one model per team exists
        single_model_per_team = len(crewmate_models) == 1 and len(impostor_models) == 1

        # Summary function with conditional header and model listing
        def summarize_team(team, team_name, models):
            model_names = ", ".join(models)
            header_text = f"Summary for {team_name} - Model: {model_names}" if single_model_per_team else f"Summary for {team_name}"
            st.subheader(header_text)
            if not single_model_per_team:
                st.write(f"Models used: {model_names}")

            st.write(f"Number of {team_name.lower()}: {len(team)}")
            st.write("Players:", ", ".join([p.name for p in team]))

            total_techniques = sum(len(player_techniques[p.name]) for p in team)
            avg_techniques = total_techniques / len(team) if team else 0
            st.write(f"Total techniques: {total_techniques}")
            st.write(f"Average techniques per player: {avg_techniques:.2f}")

            # Technique breakdown for the team
            all_team_techniques = [tech for p in team for tech in player_techniques[p.name]]
            team_technique_counts = Counter(all_team_techniques)
            st.markdown("**Technique breakdown:**")
            for technique, count in team_technique_counts.items():
                avg_per_player = count / len(team) if team else 0
                st.write(f" - {technique}: {count} times - (avg per player: {avg_per_player:.2f})")

        # Summaries for crewmates and impostors
        summarize_team(crewmates, "Crewmates", crewmate_models)
        summarize_team(impostors, "Impostors", impostor_models)

        # Add model summary if multiple models are used within teams
        if not single_model_per_team:
            st.subheader("Summary by Model")
            models = defaultdict(list)
            for player in players:
                models[player.llm_model_name].append(player)

            for model_name, model_players in models.items():
                st.markdown(f"### Model: {model_name}")
                st.write(f"Number of players: {len(model_players)}")
                st.write("Players:", ", ".join([p.name for p in model_players]))

                total_techniques = sum(len(player_techniques[p.name]) for p in model_players)
                avg_techniques = total_techniques / len(model_players) if model_players else 0
                st.write(f"Total techniques: {total_techniques}")
                st.write(f"Average techniques per player: {avg_techniques:.2f}")

                # Technique breakdown for this model
                all_model_techniques = [tech for p in model_players for tech in player_techniques[p.name]]
                model_technique_counts = Counter(all_model_techniques)
                st.markdown("**Technique breakdown:**")
                for technique, count in model_technique_counts.items():
                    avg_per_player = count / len(model_players) if model_players else 0
                    st.write(f" - {technique}: {count} times (avg per player: {avg_per_player:.2f})")

    def _display_player_selection(self, players: List[Player]):
        selected_player = st.radio(
            "Select Player",
            [len(players)] + list(range(len(players))),
            horizontal=True,
            key=f"player_selection_{players}",
            format_func=lambda i: players[i].name if i < len(players) else "None",
        )
        # st.write(f"Selected Player: {players[selected_player].name if selected_player < len(players) else 'All'}")
        st.session_state.selected_player = selected_player
    
    def _display_discussion_chat(self, players: List[Player]):
        discussion_chat = ""
        if st.session_state.selected_player == len(players):
            for player in players:
                if player.state.life == PlayerState.ALIVE:
                    discussion_chat = "\n".join(player.get_chat_messages())
                    break
        else:
            player = players[st.session_state.selected_player]
            discussion_chat = "\n".join([x for x in player.get_chat_messages() if x.startswith(f"[{player.name}]")])
        st.text_area(label="Discussion log:", value=discussion_chat)
        return discussion_chat

    def get_cost_data(self, game_engine: GameEngine) -> Dict[str, List[float]]:
        """Extracts cost data from player history."""
        cost_data = {}
        for player in game_engine.state.players:
            costs = [round(r.token_usage.cost, 4) for r in player.history.rounds]
            cost_data[player.name] = costs
        return cost_data

    def estimate_future_cost(self, cost_data: Dict[str, List[float]], rounds_to_forecast: int, degree: int = 2) -> Dict[str, List[float]]:
        """Estimates future cost using polynomial regression for each player."""
        estimated_cost_data = {}
        for player_name, costs in cost_data.items():
            # Prepare data for linear regression
            X = [[i] for i in range(len(costs))]
            y = costs

            # Create polynomial features
            poly = PolynomialFeatures(degree=degree)
            X_poly = poly.fit_transform(X)

            # Train a separate model for each player
            model = LinearRegression()
            model.fit(X_poly, y)

            # Estimate future costs
            future_rounds = [[i] for i in range(len(costs), len(costs) + rounds_to_forecast)]
            future_rounds_poly = poly.transform(future_rounds)
            estimated_costs = [round(model.predict([future_round])[0], 4) for future_round in future_rounds_poly]
            estimated_cost_data[player_name] = estimated_costs
        return estimated_cost_data

    def combine_data(self, cost_data: Dict[str, List[float]], estimated_cost_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """Combines actual and estimated cost data."""
        combined_cost_data = {}
        for player_name in cost_data:
            combined_cost_data[player_name] = cost_data[player_name] + estimated_cost_data[player_name]
        return combined_cost_data

    def plot_cost(self, cost_data: Dict[str, List[float]], rounds_to_forecast: int):
        """Plots cost data using Plotly."""
        fig = go.Figure()
        history = list(cost_data.values())[0]

        for player_name, costs in cost_data.items():
            # Separate actual and estimated costs
            actual_costs = costs[:len(history)-rounds_to_forecast]
            estimated_costs = costs[len(history)-rounds_to_forecast:]

            # Plot actual costs as solid lines
            fig.add_trace(go.Scatter(x=list(range(1, len(actual_costs) + 1)), y=actual_costs, name=player_name, mode='lines'))

            # Plot estimated costs as dashed lines
            fig.add_trace(go.Scatter(x=list(range(len(actual_costs), len(costs)+1)), y=[actual_costs[-1]]+estimated_costs, name=player_name, mode='lines', line=dict(dash='dash')))

        # Calculate total cost
        total_costs = [sum(costs[i] for costs in cost_data.values()) for i in range(len(history))]
        
        # Separate actual and estimated total costs
        actual_total_costs = total_costs[:len(history)-rounds_to_forecast]
        estimated_total_costs = total_costs[len(history)-rounds_to_forecast:]

        # Plot actual total cost as solid lines
        fig.add_trace(go.Scatter(x=list(range(1, len(actual_total_costs) + 1)), y=actual_total_costs, name="Total Cost", mode='lines'))

        # Plot estimated total cost as dashed lines
        fig.add_trace(go.Scatter(x=list(range(len(actual_total_costs), len(total_costs)+1)), y=[actual_total_costs[-1]]+estimated_total_costs, name="Total Cost", mode='lines', line=dict(dash='dash')))

        fig.update_layout(
            title="Player Cost Over Rounds",
            xaxis_title="Round Number",
            yaxis_title="Cost",
            legend_title="Players"
        )

        st.plotly_chart(fig)

    def _display_chat_history(self, rounds: List[RoundData]):
        """Displays the chat history for a player using st.chat_message."""
        with st.container(height=500, border=True):
            for round_data in rounds:
                # 1. Prompt (Player Message)
                with st.chat_message("user"):
                    with st.expander("Prompt"):
                        st.write(round_data.prompt)

                # 2. Actions (System Message)
                if round_data.actions:  # Check if actions exist
                    with st.chat_message("system"):
                        st.write("Actions:")
                        for i, action in enumerate(round_data.actions):
                            st.write(f"{i}. {action}")

                # 3. Response (LLM Message)
                for llm_response in round_data.llm_responses:
                    with st.chat_message("assistant"):
                        with st.expander("LLM Response"):  # Put llm_responses in expander
                            st.write(llm_response)
                    
                # 4. Response
                with st.chat_message("assistant"):
                    st.write(round_data.response)

                # 4. Action Result (System Message)
                if round_data.action_result:  # Check if action result exists
                    with st.chat_message("system"):
                        st.write(f"Action Result: {round_data.action_result}")
