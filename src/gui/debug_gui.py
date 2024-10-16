import tkinter as tk
from tkinter import ttk
from game.game_engine import GameEngine
import threading

class DebugGUI:
    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine
        self.window = tk.Tk()
        self.window.title("Among Us Debugger")

        # Create player dashboard tabs
        self.player_tabs = ttk.Notebook(self.window)
        for player in self.game_engine.players:
            player_frame = tk.Frame(self.player_tabs)
            self.create_player_panel(player_frame, player)
            self.player_tabs.add(player_frame, text=player.name)
        self.player_tabs.pack()

        # Create AI agent response window
        self.agent_response_window = tk.Toplevel(self.window)
        self.agent_response_window.title("AI Agent Responses")
        self.agent_response_text = tk.Text(self.agent_response_window)
        self.agent_response_text.pack()       
                                                                                                                
        # Start the game loop in a separate thread                                                                                                                      
        game_thread = threading.Thread(target=self.game_engine.main_game_loop)                                                                                                      
        game_thread.start()

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
        player_location_label = tk.Label(frame, text=f"Location: {player.player_location}")
        player_location_label.pack()

        # Task List
        task_list_label = tk.Label(frame, text="Tasks:")
        task_list_label.pack()
        self.task_listbox = tk.Listbox(frame)
        for task in player.player_tasks:
            self.task_listbox.insert(tk.END, str(task))
        self.task_listbox.pack()

        # Action History
        action_history_label = tk.Label(frame, text="Action History:")
        action_history_label.pack()
        self.action_history_text = tk.Text(frame)
        self.action_history_text.pack()

        # Chat History
        chat_history_label = tk.Label(frame, text="Chat History:")
        chat_history_label.pack()
        self.chat_history_text = tk.Text(frame)
        self.chat_history_text.pack()

        # AI Agent Responses
        agent_responses_label = tk.Label(frame, text="AI Agent Responses:")
        agent_responses_label.pack()
        self.agent_responses_text = tk.Text(frame)
        self.agent_responses_text.pack()

    def update_gui(self):
        # Update player information in the dashboard
        for i, player in enumerate(self.game_engine.players):
            # Update player name
            player_name_label = self.player_tabs.winfo_children()[i].winfo_children()[0]
            player_name_label.config(text=f"Player: {player.name}")

            # Update player role
            player_role_label = self.player_tabs.winfo_children()[i].winfo_children()[1]
            player_role_label.config(text=f"Role: {player.role}")

            # Update player state
            player_state_label = self.player_tabs.winfo_children()[i].winfo_children()[2]
            player_state_label.config(text=f"State: {player.player_state}")

            # Update player location
            player_location_label = self.player_tabs.winfo_children()[i].winfo_children()[3]
            player_location_label.config(text=f"Location: {player.player_location}")

            # Update task list
            task_listbox = self.player_tabs.winfo_children()[i].winfo_children()[5]
            task_listbox.delete(0, tk.END)
            for task in player.player_tasks:
                task_listbox.insert(tk.END, str(task))

            # Update action history
            action_history_text = self.player_tabs.winfo_children()[i].winfo_children()[7]
            action_history_text.delete("1.0", tk.END)
            for action in player.history:
                action_history_text.insert(tk.END, f"{action}\n")

            # Update chat history
            chat_history_text = self.player_tabs.winfo_children()[i].winfo_children()[9]
            chat_history_text.delete("1.0", tk.END)
            for message in player.chat_history:
                chat_history_text.insert(tk.END, f"{message}\n")

            # Update AI agent responses
            agent_responses_text = self.player_tabs.winfo_children()[i].winfo_children()[11]
            agent_responses_text.delete("1.0", tk.END)
            for response in player.history:
                agent_responses_text.insert(tk.END, f"{response}\n")

        # Update AI agent responses in the separate window
        self.agent_response_text.delete("1.0", tk.END)
        for player in self.game_engine.players:
            for response in player.history:
                self.agent_response_text.insert(tk.END, f"{player.name}: {response}\n")

        self.window.after(100, self.update_gui)

    def run(self):
        self.window.mainloop()

# # Example usage
# game = GameEngine()
# # ... (Load players and initialize the game)
# gui = DebugGUI(game)
# gui.run()
