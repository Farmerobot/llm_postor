import json
import os
import pandas as pd


dir = 'data/tournament'
files = list(os.walk(dir))[0][2]

columns = ["imp_model", "crew_model", "imp_out_tokens", "crew_out_tokens", "rounds", "result", "imp_pretend_count"]
data = []

for f in files:
    with open(dir + '/' + f) as file:
        d = json.load(file)
        imp_model = f.split(".")[0].split("_")[0]
        crew_model = f.split(".")[0].split("_")[2]
        imp_out_tokens, crew_out_tokens = 0, 0
        rounds = len(d["players"][0]["history"]["rounds"])

        if "_round_limit" in f:
            res = "lim"
        elif "Crewmates win!" in d["playthrough"][-1]:
            res = "crew"
        else:
            res = "imp"

        for i in range(5):
            p = d["players"][i]
            if p["role"] == "Impostor":
                imp_out_tokens += p["state"]["token_usage"]["output_tokens"]

                imp_pretend = 1 if "pretended" in p["state"]["action_result"] else 0
                for round in p["history"]["rounds"]:
                    if "pretended" in round["action_result"]:
                        imp_pretend += 1
            else:
                crew_out_tokens += p["state"]["token_usage"]["output_tokens"]
        data.append([imp_model, crew_model, imp_out_tokens, crew_out_tokens, rounds, res, imp_pretend])


df = pd.DataFrame(data, columns=columns)
df.to_csv("token_usage.csv")

print(df)