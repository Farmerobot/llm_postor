from game.models.engine import GameLocation, GamePhase
from game.models.history import PlayerState
from game.players.base_player import Player
from typing import List
from pydantic import BaseModel, Field


class GameState(BaseModel):
    players: List[Player] = Field(default_factory=list)
    game_stage: GamePhase = GamePhase.MAIN_MENU
    playthrough: List[str] = Field(default_factory=list)
    save_playthrough: str = ""
    DEBUG: bool = Field(default=False)
    round_number: int = 0
    player_to_act_next: int = 0
    round_of_discussion_start: int = 0

    def add_player(self, player: Player):
        self.players.append(player)

    def set_stage(self, stage: GamePhase):
        if stage == self.game_stage:
            print(f"Game is already in stage {stage}. Skipping")
            return
        self.game_stage = stage
        for player in self.players:
            player.set_stage(stage)
        if stage == GamePhase.DISCUSS:
            self.player_to_act_next = 0
            self.round_of_discussion_start = self.round_number
        elif stage == GamePhase.ACTION_PHASE:
            self.player_to_act_next = 0

    def log_action(self, action: str):
        self.playthrough.append(action)
        if self.DEBUG:
            print(action)

    def get_alive_players(self) -> List[Player]:
        return [p for p in self.players if p.state.life == PlayerState.ALIVE]

    def get_dead_players(self) -> List[Player]:
        return [p for p in self.players if p.state.life == PlayerState.DEAD]

    def get_dead_players_in_location(self, location: GameLocation) -> List[Player]:
        return [
            p
            for p in self.players
            if p.state.life == PlayerState.DEAD and p.state.location == location
        ]

    def get_players_in_location(self, location: GameLocation) -> List[Player]:
        return [p for p in self.players if p.state.location == location and p.state.life == PlayerState.ALIVE]

    def get_player_targets(self, player: Player) -> List[Player]:
        return [
            other_player
            for other_player in self.players
            if other_player != player
            and other_player.state.life == PlayerState.ALIVE
            and other_player.state.location == player.state.location
        ]
        
    def get_total_cost(self) -> int:
        output = {}
        for player in self.players:
            output[f"{player.name}_cost"] = player.state.token_usage.cost
        total_cost = sum(output.values())
        output["total_cost"] = total_cost
        output["average_per_round"] = total_cost / (self.round_number+1)
        output["average_per_player"] = total_cost / len(self.players)
        output["average_per_round_per_player"] = total_cost / (len(self.players) * (self.round_number) + self.player_to_act_next + 1)
        return output
        
            

    def to_dict(self):
        return {
            "players": [player.to_dict() for player in self.players],
            "game_stage": self.game_stage.value,
            "playthrough": self.playthrough,
            "save_playthrough": self.save_playthrough,
            "DEBUG": self.DEBUG,
            "round_number": self.round_number,
            "current_player_index": self.player_to_act_next,
        }
