from typing import List
from pydantic import BaseModel, Field

from game.models.game_models import GameLocation, GamePhase, PlayerState, Task

class RoundData(BaseModel):
    location: GameLocation = GameLocation.LOC_CAFETERIA
    stage: GamePhase = GamePhase.MAIN_MENU
    life: PlayerState = PlayerState.ALIVE
    tasks: List[Task] = Field(default_factory=list)
    llm_responses: List[str] = Field(default_factory=list)
    prompt: str = ""
    actions: List[str] = Field(default_factory=list)
    response: str = ""
    action_result: str = ""
    seen_actions: List[str] = Field(default_factory=list)
    player_in_room: str = ""
    observations: List[str] = Field(default_factory=list)
    
class PlayerHistory(BaseModel):
    rounds: List[RoundData] = Field(default_factory=list)

    def add_round(self, round_data: RoundData):
        self.rounds.append(round_data)

    def get_history(self) -> List[RoundData]:
        return self.rounds
    
    def get_history_str(self) -> str:
        history_str = ""
        for i, round in enumerate(self.rounds):
            seen_actions = ', '.join(round.seen_actions)
            observations = ', '.join(round.observations)
            history_str += f"Round {i+1}\n"
            history_str += f"Location: {round.location}\n"
            history_str += f"Seen Actions: {seen_actions}\n"
            history_str += f"Players in Room: {round.player_in_room}\n"
            history_str += f"Observations: {observations}\n"
        return history_str
