from game.game_engine import GameEngine
from game.models.player import Player
from game.models.game_models import GamePhase, PlayerRole

turns_to_complete: list[int] = []
for model_name in ["gpt-4o-mini", "gpt-4o"]:
    # for model_name in ["gpt-4o", "gpt-4-32k"]:
    print(f"Model: {model_name}")
    for i in range(5, 10):
        print(f"Test {i}")

        game = GameEngine()
        players = [Player("Robot", agent="ai", model_name=model_name)]
        game.load_players(players, choose_impostor=False)
        game.init_game()
        game.DEBUG = True
        game.save_playthrough = f"Test_crewmate_action_{model_name}_{i}.txt"
        print(game.players[0].player_tasks)
        game.main_game_loop(GamePhase.ACTION_PHASE)
        turns_to_complete.append(
            max([player.turns_passed() for player in game.players])
        )
        print("End of test")

    print(f"turns_to_complete: {turns_to_complete}")
    print(
        f"Average turns to complete: {sum(turns_to_complete) / len(turns_to_complete)}"
    )
    print(f"Max turns to complete: {max(turns_to_complete)}")
    print(f"Min turns to complete: {min(turns_to_complete)}")
    with open(
        f"./game/game_results/action_phase/turns_to_complete_crewmate_action_{model_name}.txt",
        "w+",
    ) as f:
        f.write(str(turns_to_complete))
        f.write(
            f"\nAverage turns to complete: {sum(turns_to_complete) / len(turns_to_complete)}"
        )
        f.write(f"\nMax turns to complete: {max(turns_to_complete)}")
        f.write(f"\nMin turns to complete: {min(turns_to_complete)}")
    turns_to_complete = []
