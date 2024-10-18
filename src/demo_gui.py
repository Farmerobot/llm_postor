from game.game_engine import GameEngine
from game.models.player_human import HumanPlayer
from game.models.player_ai import AIPlayer
from game.models.game_models import PlayerRole
from game.gui.debug_gui import DebugGUI

game = GameEngine()

model_name = "gpt-4o-mini"
# model_name = "gemini-1.5-flash"

# impostor = HumanPlayer(name="Warcin")
impostor = AIPlayer(name="Warcin", llm_model_name=model_name)
impostor.set_role(PlayerRole.IMPOSTOR)

players = [
    AIPlayer(name="Wateusz", llm_model_name=model_name),
    AIPlayer(name="Waciej", llm_model_name=model_name),
    AIPlayer(name="Warek", llm_model_name=model_name),
    AIPlayer(name="Wikolaj", llm_model_name=model_name),
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

