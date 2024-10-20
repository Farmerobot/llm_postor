from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator
from game.models.game_models import (
    GamePhase,
    PlayerRole,
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
    name: str
    role: PlayerRole = PlayerRole.CREWMATE
    is_impostor: bool = False
    kill_cooldown: int = 0
    state: RoundData = Field(default_factory=RoundData)
    history: PlayerHistory = Field(default_factory=PlayerHistory)
    adventure_agent: Optional[AdventureAgent] = None
    discussion_agent: Optional[DiscussionAgent] = None
    voting_agent: Optional[VotingAgent] = None
    
    @model_validator(mode='after')
    def post_update(self) -> 'Player':
        if self.role == PlayerRole.IMPOSTOR:
            self.is_impostor = True
            self.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
            self.state.tasks = [ShortTask(name="Eliminate all crewmates", location=GameLocation.LOC_UNKNOWN)]
        else:
            self.is_impostor = False
            self.kill_cooldown = 0
            self.state.tasks = get_random_tasks()
        return self

    def set_stage(self, stage: GamePhase) -> None:
        self.state.stage = stage
        if stage == GamePhase.ACTION_PHASE:
            self.state.location = GameLocation.LOC_CAFETERIA

    def get_task_to_complete(self) -> List[Task]:
        return [task for task in self.state.tasks if not task.completed]

    def log_state_new_round(self) -> None:
        self.history.add_round(self.state)
        self.state.tasks = [task for task in self.state.tasks if not task.completed]
        self.state.llm_responses = []
        self.state.prompt = ""
        self.state.actions = []
        self.state.response = ""
        self.state.action_result = ""
        self.state.seen_actions = []
        self.state.player_in_room = ""
        self.state.observations = []

    @abstractmethod
    def prompt_action(self, actions: List[str]) -> int:
        pass

    @abstractmethod
    def prompt_discussion(self) -> str:
        pass

    @abstractmethod
    def prompt_vote(self, voting_actions: List[str]) -> int:
        pass

    def get_message_str(self) -> str:
        return "\n".join(self.state.chat_history[-1])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
