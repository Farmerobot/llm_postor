from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from llm_postor.game.models.engine import GameLocation, GamePhase
from llm_postor.game.models.tasks import Task
from llm_postor.game.agents.usage_metadata import UsageMetadata

class PlayerState(str, Enum):
    ALIVE = "Alive"
    DEAD = "Dead"
    DEAD_REPORTED = "Dead Reported"


class RoundData(BaseModel):
    location: GameLocation = GameLocation.LOC_CAFETERIA
    stage: GamePhase = GamePhase.MAIN_MENU # purely for ease of debugging
    life: PlayerState = PlayerState.ALIVE
    tasks: List[Task] = Field(default_factory=list)
    llm_responses: List[str] = Field(default_factory=list)
    token_usage: UsageMetadata = Field(default_factory=UsageMetadata)
    prompt: str = ""
    actions: List[str] = Field(default_factory=list)
    response: str = ""
    action_result: str = ""
    seen_actions: List[str] = Field(default_factory=list)
    player_in_room: str = ""
    observations: List[str] = Field(default_factory=list)

    def to_dict(self):
        return {
            "location": self.location.value,
            "stage": self.stage.value,
            "life": self.life.value,
            "token_usage": self.token_usage.to_dict(),
            "tasks": [str(task) for task in self.tasks],
            "llm_responses": self.llm_responses,
            "prompt": self.prompt,
            "actions": self.actions,
            "response": self.response,
            "action_result": self.action_result,
            "seen_actions": self.seen_actions,
            "player_in_room": self.player_in_room,
            "observations": self.observations,
        }


class PlayerHistory(BaseModel):
    rounds: List[RoundData] = Field(
        default_factory=lambda: [
            RoundData(
                location=GameLocation.LOC_CAFETERIA,
                stage=GamePhase.MAIN_MENU,
                life=PlayerState.ALIVE,
            )
        ]
    )

    def add_round(self, round_data: RoundData):
        self.rounds.append(round_data)

    def get_history(self) -> List[RoundData]:
        return self.rounds

    def get_history_str(self) -> str:
        history_str = ""
        for i, round in enumerate(self.rounds):
            seen_actions = ", ".join(round.seen_actions)
            observations = ", ".join(round.observations)
            history_str += f"Round {i+1}\n"
            history_str += f"Location: {round.location}\n"
            history_str += f"Seen Actions: {seen_actions}\n"
            history_str += f"Players in Room: {round.player_in_room}\n"
            history_str += f"Observations: {observations}\n"
        return history_str

    def to_dict(self):
        return {"rounds": [round_data.to_dict() for round_data in self.rounds]}
