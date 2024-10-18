from abc import ABC, abstractmethod
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from game.models.game_models import (
    GamePhase,
    PlayerRole,
    PlayerState,
    GameLocation,
    Task,
    ShortTask,
)
import game.consts as game_consts
from game.utils import get_random_tasks
from .player_history import PlayerHistory, RoundData
from game.agents.adventure_agent import AdventureAgent
from game.agents.discussion_agent import DiscussionAgent
from game.agents.voting_agent import VotingAgent


class Player(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    role: PlayerRole = PlayerRole.CREWMATE
    stage: GamePhase = GamePhase.MAIN_MENU
    state: PlayerState = PlayerState.ALIVE
    location: GameLocation = GameLocation.LOC_CAFETERIA
    tasks: List[Task] = [ShortTask("Eliminate all crewmates", GameLocation.LOC_UNKNOWN)] if role == PlayerRole.IMPOSTOR else get_random_tasks()
    can_vote: bool = False
    kill_cooldown: int = 0
    history: PlayerHistory = Field(default_factory=PlayerHistory)
    responses: List[str] = Field(default_factory=list)
    chat_history: List[Any] = Field(default_factory=list)
    prev_location: Optional[GameLocation] = None
    discussion_prompt: str = ""
    is_impostor: bool = False
    adventure_agent: Optional[AdventureAgent] = None
    discussion_agent: Optional[DiscussionAgent] = None
    voting_agent: Optional[VotingAgent] = None

    def set_role(self, role: PlayerRole) -> None:
        self.role = role
        if role == PlayerRole.IMPOSTOR:
            self.is_impostor = True
            self.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
            self.tasks = [ShortTask("Eliminate all crewmates", GameLocation.LOC_UNKNOWN)]
        else:
            self.is_impostor = False

    def set_stage(self, stage: GamePhase) -> None:
        self.stage = stage
        if stage == GamePhase.DISCUSS:
            self.can_vote = True
        if stage == GamePhase.ACTION_PHASE:
            self.can_vote = False
            self.location = GameLocation.LOC_CAFETERIA

    def get_task_to_complete(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]

    def log_round(self, observations: List[str], llm_responses: List[str], actions: List[str]):
        round_data = RoundData(location=self.location.value, observations=observations, llm_responses=llm_responses, actions=actions)
        self.history.add_round(round_data)

    @abstractmethod
    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        pass

    @abstractmethod
    def prompt_discussion(self) -> str:
        pass

    @abstractmethod
    def prompt_vote(self, voting_actions: List[str]) -> int:
        pass

    def get_message_str(self) -> str:
        return "\n".join(self.chat_history[-1])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
