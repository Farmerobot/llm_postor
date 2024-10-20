from game.models.game_models import GamePhase, PlayerState
from game.models.player import Player
from typing import List
from pydantic import BaseModel, Field


class GameState(BaseModel):
    players: List[Player] = Field(default_factory=list)
    game_stage: GamePhase = GamePhase.MAIN_MENU
    playthrough: List[str] = Field(default_factory=list)
    save_playthrough: str = ""
    DEBUG: bool = Field(default=False)

    def add_player(self, player: Player):
        self.players.append(player)

    def set_stage(self, stage: GamePhase):
        self.game_stage = stage
        for player in self.players:
            player.set_stage(stage)

    def log_action(self, action: str):
        self.playthrough.append(action)

    def get_alive_players(self) -> List[Player]:
        return [p for p in self.players if p.state.life == PlayerState.ALIVE]

    def get_dead_players(self) -> List[Player]:
        return [p for p in self.players if p.state.life == PlayerState.DEAD]

    def get_dead_players_in_location(self, location: int) -> List[Player]:
        return [
            p
            for p in self.players
            if p.state == PlayerState.DEAD and p.location == location
        ]

    def get_player_targets(self, player: Player) -> List[Player]:
        return [
            other_player
            for other_player in self.players
            if other_player != player
            and other_player.state.life == PlayerState.ALIVE
            and other_player.state.location == player.state.location
        ]
