import tkinter as tk
from tkinter import ttk
from game.game_engine import GameEngine
from game.models.game_models import GamePhase
from game.models.game_models import GamePhase
import threading


class DebugGUI:
    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine
        self.window = tk.Tk()
        self.window.title("Among Us Debugger")
        # Create player dashboard tabs
        self.player_tabs = ttk.Notebook(self.window)
        for player in self.game_engine.state.players:
            player_frame = tk.Frame(self.player_tabs)
            self.create_player_panel(player_frame, player)
            self.player_tabs.add(player_frame, text=player.name)
        self.player_tabs.pack()
        # Create AI agent response window
        self.agent_responses_window = tk.Toplevel(self.window)
        self.agent_responses_window.title("AI Agent Responses")
        self.agent_responses_text = tk.Text(self.agent_responses_window)
        self.agent_responses_text.pack()
        # Update GUI with game state changes
        self.update_gui()
    def create_player_panel(self, frame, player):
        # Player Name
        player_name_label = tk.Label(frame, text=f"Player: {player.name}")
        player_name_label.pack()
        # Player Role
        player_role_label = tk.Label(frame, text=f"Role: {player.role}")
        player_role_label.pack()
        # Player State
        player_state_label = tk.Label(frame, text=f"State: {player.player_state}")
        player_state_label.pack()
        # Player Location
        player_location_label = tk.Label(
            frame, text=f"Location: {player.player_location}"
        )
        player_location_label.pack()
        # Task List
        task_list_label = tk.Label(frame, text="Tasks:")
        task_list_label.pack()
        task_listbox = tk.Listbox(frame)
        for task in player.player_tasks:
            task_listbox.insert(tk.END, str(task))
        task_listbox.pack()
        # Action History
        action_history_label = tk.Label(frame, text="Action History:")
        action_history_label.pack()
        action_history_text = tk.Text(frame)
        action_history_text.pack()
        # AI Agent Responses
        agent_response_label = tk.Label(frame, text="AI Agent Response:")
        agent_response_label.pack()
        agent_response_text = tk.Text(frame)
        agent_response_text.pack()
        # Chat History
        chat_history_label = tk.Label(frame, text="Chat History:")
        chat_history_label.pack()
        chat_history_text = tk.Text(frame)
        chat_history_text.pack()
    def update_gui(self):
        # Update player information in the dashboard
        for i, player in enumerate(self.game_engine.state.players):
            # Update player name
            player_name_label = self.player_tabs.winfo_children()[i].winfo_children()[0]
            player_name_label.config(text=f"Player: {player.name}")
            # Update player role
            player_role_label = self.player_tabs.winfo_children()[i].winfo_children()[1]
            player_role_label.config(text=f"Role: {player.role}")
            # Update player state
            player_state_label = self.player_tabs.winfo_children()[i].winfo_children()[
                2
            ]
            player_state_label.config(text=f"State: {player.player_state}")
            # Update player location
            player_location_label = self.player_tabs.winfo_children()[
                i
            ].winfo_children()[3]
            player_location_label.config(text=f"Location: {player.player_location}")
            # Update task list
            task_listbox = self.player_tabs.winfo_children()[i].winfo_children()[5]
            task_listbox.delete(0, tk.END)
            for task in player.player_tasks:
                task_listbox.insert(tk.END, str(task))
            # Update action history
            action_history_text = self.player_tabs.winfo_children()[i].winfo_children()[
                7
            ]
            action_history_text.delete("1.0", tk.END)
            history_str = ""
            for entry in player.history:
                for key, value in entry.items():
                    if isinstance(value, list):
                        joined_value = "\n".join(value)
                        history_str += f"{key}: {joined_value}\n"
                    else:
                        history_str += f"{key}: {value}\n"
                history_str += "\n"
            action_history_text.insert(tk.END, history_str)
            # Update chat history
            chat_history_text = self.player_tabs.winfo_children()[i].winfo_children()[11]
            chat_history_text.delete("1.0", tk.END)
            chat_history_str = ""
            for message in player.chat_history:
                chat_history_str += f"{message}\n"
            chat_history_text.insert(tk.END, chat_history_str)
            # Update AI agent responses
            agent_response_text = self.player_tabs.winfo_children()[i].winfo_children()[9]
            agent_response_text.delete("1.0", tk.END)
            agent_response_text.insert(tk.END, "Adventure Agent Responses:\n")
            if player.adventure_agent and player.adventure_agent.responses:
                for response in player.adventure_agent.responses:
                    agent_response_text.insert(tk.END, f"{response}\n\n")
            if player.discussion_agent and player.discussion_agent.responses:
                for response in player.discussion_agent.responses:
                    agent_response_text.insert(tk.END, f"Responses: {response}\n\n")
            if player.voting_agent and player.voting_agent.responses:
                for response in player.voting_agent.responses:
                    agent_response_text.insert(tk.END, f"Responses: {response}\n\n")
        # Update AI agent responses in the separate window
        self.agent_responses_text.delete("1.0", tk.END)
        for player in self.game_engine.state.players:
            for response in player.history:
                for key, value in response.items():
                    if isinstance(value, list):
                        joined_value = "\n".join(value)
                        self.agent_responses_text.insert(tk.END, f"{player.name} {key}: {joined_value}\n")
                    else:
                        self.agent_responses_text.insert(tk.END, f"{player.name} {key}: {value}\n")

        self.window.update()
    def run(self):
        self.window.mainloop()
