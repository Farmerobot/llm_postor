import pandas as pd
import os

# Variables
n_repetitions=5
n_players = 5
n_impostors = 1
dir = 'data/tournament'
n_round_cut_off = 40
debug = False
ai_models = [
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-405b-instruct",
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "google/gemini-flash-1.5",
    "google/gemini-pro-1.5",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-5-haiku"
]
n_ai_models = 8
idx, parts = 1, 1

OUTPUT = []

file_names = list(os.walk(dir))[0][2]


def get_game_permutations():
    permutes = []

    for i in range(n_ai_models):
        for j in range(n_ai_models):
            for repetition in range(n_repetitions):
                permutes.append((i, j, repetition))

    n = len(permutes) // parts

    if idx == parts:
        return permutes[n*(idx-1):]
    
    return permutes[n*(idx-1):n*idx]

set_ij = set()

for i, j, _ in get_game_permutations():
    if (i, j) in set_ij:
        continue
    set_ij.add((i, j))
    wins, loses, round_limits, exceptions, game_prices = 0, 0, 0, 0, [0 for _ in range(n_repetitions)]
    for repetition in range(n_repetitions):
        file_path_pattern=(
            ai_models[i].split("/")[-1].replace(".", "-") +
            "_vs_" +
            ai_models[j].split("/")[-1].replace(".", "-") +
            "_" +
            str(repetition + 1)
        )

        file_path = ''
        occurence = filter(lambda x: file_path_pattern in x, file_names)
        if res := list(occurence):
            file_path = dir + "/" + res[0]
        else:
            continue

        # game_engine = GameEngine()
        # game_engine.load_state(file_path)

        if "exception" in file_path:
            exceptions += 1
        elif "round_limit" in file_path:
            round_limits += 1
        else:
            with open(file_path, 'r') as file:
                text = file.read()
                if "Crewmates win! All impostors were banished!" in text:
                    loses += 1
                else:
                    wins += 1

        # game_prices[repetition] = game_engine.state.get_total_cost()["total_cost"]
    
    OUTPUT.append([
        ai_models[i].split('/')[-1].replace('.', '-'), ai_models[j].split('/')[-1].replace('.', '-'),
        wins, loses, exceptions, round_limits
    ])
    
    print(f"{ai_models[i].split('/')[-1].replace('.', '-')} vs {ai_models[j].split('/')[-1].replace('.', '-')}")

output_pd = pd.DataFrame(OUTPUT, columns=["Impostor", "Crewmate", "Wins", "Loses", "Exceptions", "Round limits"])
output_pd.to_csv("tournament_analysis.csv")
print(output_pd)
print(output_pd["Exceptions"].sum())