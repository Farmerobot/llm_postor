from itertools import permutations
from llm_postor.game.game_engine import GameEngine
import pandas as pd
import os

# Variables
n_repetitions=3
n_players = 5
n_impostors = 1
dir = 'data/tournament'
n_round_cut_off = 40
debug = False
ai_models = [
    "openai/gpt-4o-mini",
    "google/gemini-flash-1.5",
    "meta-llama/llama-3.1-70b-instruct"
]

OUTPUT = []

file_names = list(os.walk(dir))[0][2]

for i, j in permutations(range(len(ai_models)), 2):
    wins, loses, round_limits, exceptions, game_prices = 0, 0, 0, 0, [0 for _ in range(n_repetitions)]
    for repetition in range(n_repetitions):
        file_path_pattern=(
            ai_models[i].split("/")[-1].replace(".", "-") +
            "_vs_" +
            ai_models[j].split("/")[-1].replace(".", "-") +
            "_" +
            str(repetition + 1)
        )
        file_path = dir + "/" + next(filter(lambda x: file_path_pattern in x, file_names))

        game_engine = GameEngine()
        game_engine.load_state(file_path)

        if "exception" in file_path:
            exceptions += 1
        elif "round_limit" in file_path:
            round_limits += 1
        else:
            if game_engine.check_impostors_win():
                wins += 1
            else:
                loses += 1

        game_prices[repetition] = game_engine.state.get_total_cost()["total_cost"]
    
    OUTPUT.append([
        ai_models[i].split('/')[-1].replace('.', '-'), ai_models[j].split('/')[-1].replace('.', '-'),
        wins, loses, exceptions, round_limits, sum(game_prices) / len(game_prices)
    ])
    
    print(f"{ai_models[i].split('/')[-1].replace('.', '-')} vs {ai_models[j].split('/')[-1].replace('.', '-')}")

output_pd = pd.DataFrame(OUTPUT, columns=["Impostor", "Crewmate", "Wins", "Loses", "Exceptions", "Round limits", "Average game price"])
output_pd.to_csv("tournament_analysis.csv")
print(output_pd)