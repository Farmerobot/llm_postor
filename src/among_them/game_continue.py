from among_them.game.game_engine import GameEngine

game_engine = GameEngine(file_path="data/game_state.json")
game_engine.load_game()
game_engine.state.DEBUG = True

res = False
while not res:
    try:
        res = game_engine.perform_step()  # game is finished
    except Exception as e:
        if "LLM did" in str(e):
            continue
        else:
            raise e
