from game.game_engine import GameEngine
from game.models.player import Player
from game.models.game_models import GamePhase, PlayerRole


for i in range(10):
    print(f"Test {i}")
    
    game = GameEngine()
    impostor = Player("Warcin", agent="ai", model_name="gpt-4o")
    impostor.set_role(PlayerRole.IMPOSTOR)

    players = [Player("Wateusz", agent="ai", model_name="gpt-4o"), 
               Player("Waciej", agent="ai", model_name="gpt-4o"), 
               Player("Warek", agent="ai", model_name="gpt-4o"), 
               Player("Wikolaj", agent="ai", model_name="gpt-4o"), 
               impostor]
    game.load_players(players, choose_impostor=False)
    game.init_game()
    game.DEBUG = True
    game.save_playthrough = f"whole_game_test_{i}.txt"
    game.main_game_loop()
    crewmates_won = game.check_crewmates_win()
    impostor_won = game.check_impostors_win()
    print("Crewmates won" if crewmates_won else "Impostor won")    
    print("End of test")