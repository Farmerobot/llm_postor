import shutil
import streamlit as st
from llm_postor.game.consts import STATE_FILE
from llm_postor.game.game_engine import GameEngine
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.models.engine import GamePhase
import os
from random import shuffle
from itertools import permutations


# Variables
n_repetitions=3
n_players = 5
n_impostors = 1
dir = 'data/tournament'
n_round_cut_off = 40
debug = False
ai_models = [
    "meta-llama/llama-3.1-8b-instruct",
    "openai/gpt-4o-mini",
    "google/gemini-flash-1.5"
]


class TournamentGame():
    def __init__(self, n_players, n_impostors, impostor_model, crewmate_model, dir, file_path, n_round_cut_off, debug=False):
        self.n_players = n_players
        self.n_impostors = n_impostors
        self.impostor_model = impostor_model
        self.crewmate_model = crewmate_model
        self.dir = dir
        self.file_path = file_path
        self.n_round_cut_off = n_round_cut_off
        self.debug = debug
        self.full_path = os.path.join(dir, file_path)

        self.player_names = [
            "Alice", "Bob", "Charlie", "Dave", "Erin", 
            "Fiona", "George", "Hannah", "Ian", "Judy",
            "Kevin", "Liam", "Mona", "Nina", "Oscar",
            "Paula", "Quinn", "Rita", "Steve", "Tina",
            "Uma", "Victor", "Wendy", "Xander", "Yara", "Zane"
        ][:n_players]
        shuffle(self.player_names)
        
        self.players = self.get_players()
        self.game_engine = self.get_game_engine()

    
    def get_players(self):
        return [
            AIPlayer(
                name=self.player_names[i], 
                llm_model_name=self.impostor_model if i < self.n_impostors else self.crewmate_model, 
                role="Impostor" if i < self.n_impostors else "Crewmate"
            )
            for i in range(self.n_players)
        ]
    

    def get_game_engine(self):
        game_engine = GameEngine(file_path=self.full_path)
        game_engine.state.DEBUG = self.debug
        game_engine.load_players(self.players, impostor_count=self.n_impostors)
        game_engine.state.game_stage = GamePhase.ACTION_PHASE

        return game_engine

    
    def run(self):
        res = False
        # while game is not finished and number of rounds doesn't exceed the limit
        while not res and self.game_engine.state.round_number < self.n_round_cut_off:
            try:
                res = self.game_engine.perform_step()  # game is finished
                shutil.copyfile(self.full_path, STATE_FILE)
            except Exception as e:
                if "LLM did" in str(e):
                    continue
                else:
                    try:
                        self.add_file_name_flag("exception")
                    except:
                        ...
                    with open("data/error_log.txt", "a") as file:
                        file.write(f"{self.file_path} errored with code:\n{str(e)}\n")
                    break

        if self.game_engine.state.round_number >= self.n_round_cut_off:  # too many rounds
            self.add_file_name_flag("round_limit")
        

    def add_file_name_flag(self, flag):
        new_file = self.full_path.split('.')[0] + '_' + flag + '.json'
        os.rename(self.full_path, new_file)


class Tournament():
    def __init__(self, ai_models, n_repetitions, n_players, n_impostors, dir, n_round_cut_off, debug):
        self.ai_models = ai_models
        self.n_repetitions = n_repetitions
        self.n_ai_models = len(self.ai_models)
        self.n_players = n_players
        self.n_impostors = n_impostors
        self.dir = dir
        self.n_round_cut_off = n_round_cut_off
        self.debug = debug
    

    def run(self):
        for i, j in permutations(range(self.n_ai_models), 2):
            for repetition in range(self.n_repetitions):
                print(f"Starting new game!\nGame {self.ai_models[i].split('/')[-1].replace('.', '-')} vs {self.ai_models[j].split('/')[-1].replace('.', '-')} number {repetition + 1}\n")
                game = TournamentGame(
                    n_players=self.n_players,
                    n_impostors=self.n_impostors,
                    impostor_model=self.ai_models[i],
                    crewmate_model=self.ai_models[j],
                    dir=self.dir,
                    file_path=self.ai_models[i].split("/")[-1].replace(".", "-") + 
                        "_vs_" + 
                        self.ai_models[j].split("/")[-1].replace(".", "-") + 
                        "_" + 
                        str(repetition + 1) +
                        ".json",
                    n_round_cut_off=self.n_round_cut_off,
                    debug=self.debug
                )
                game.run()
                print("\nGame finished!\n")
        print("Tournament finished!")


tournament = Tournament(
    ai_models=ai_models,
    n_repetitions=n_repetitions,
    n_players=n_players,
    n_impostors=n_impostors, 
    dir=dir,
    n_round_cut_off=n_round_cut_off,
    debug=debug
)

tournament.run()