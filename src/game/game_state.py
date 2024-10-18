from game.models.game_models import GamePhase, PlayerState
from game.models.player import Player
from typing import List

class GameState:
    def __init__(self):
        self.players: List[Player] = []
        self.game_stage: GamePhase = GamePhase.MAIN_MENU
        self.playthrough: List[str] = []

    def add_player(self, player: Player):
        self.players.append(player)

    def set_stage(self, stage: GamePhase):
        self.game_stage = stage
        for player in self.players:
            player.set_stage(stage)

    def log_action(self, action: str):
        self.playthrough.append(action)

    def get_alive_players(self) -> List[Player]:
        return [p for p in self.players if p.state == PlayerState.ALIVE]

    def get_dead_players(self) -> List[Player]:
        return [p for p in self.players if p.state == PlayerState.DEAD]
