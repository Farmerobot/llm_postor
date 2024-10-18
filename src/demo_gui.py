from game.game_engine import GameEngine
from game.models.player import HumanPlayer, AIPlayer
from game.models.game_models import GamePhase, PlayerRole
from game.gui.debug_gui import DebugGUI

game = GameEngine()

model_name = "gpt-4o-mini"
# model_name = "gemini-1.5-flash"

# impostor = HumanPlayer("Warcin")
impostor = AIPlayer("Warcin", model_name=model_name)
impostor.set_role(PlayerRole.IMPOSTOR)

players = [
    # AIPlayer("Wateusz", model_name=model_name),
    # AIPlayer("Waciej", model_name=model_name),
    AIPlayer("Warek", model_name=model_name),
    AIPlayer("Wikolaj", model_name=model_name),
    impostor,
]
game.load_players(players, impostor_count=1)
game.init_game()

game.DEBUG = True
game.save_playthrough = f"whole_game_test__new_1.txt"
gui = DebugGUI(game)
game.gui = gui
game.main_game_loop()
gui.run()

