from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from game.models.engine import (
    GamePhase,
    GameLocation,
)
import game.consts as game_consts
from game.utils import get_impostor_tasks, get_random_tasks
from game.models.tasks import Task
from game.models.history import PlayerHistory, RoundData
from game.agents.adventure_agent import AdventureAgent
from game.agents.discussion_agent import DiscussionAgent
from game.agents.voting_agent import VotingAgent
import copy

class PlayerRole(str, Enum):
    CREWMATE = "Crewmate"
    IMPOSTOR = "Impostor"
    GHOST = "Ghost"
    UNKNOWN = "Unknown"


class Player(BaseModel, ABC):
    name: str
    role: PlayerRole = Field(default=PlayerRole.CREWMATE)
    is_impostor: bool = False
    kill_cooldown: int = game_consts.IMPOSTOR_COOLDOWN
    state: RoundData = Field(default_factory=RoundData)
    history: PlayerHistory = Field(default_factory=PlayerHistory)
    adventure_agent: Optional[AdventureAgent] = None
    discussion_agent: Optional[DiscussionAgent] = None
    voting_agent: Optional[VotingAgent] = None
    llm_model_name: Optional[str] = None
    
    model_config = ConfigDict(validate_assignment=True)
    
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.set_role(self.role)
    
    def set_role(self, role: PlayerRole) -> None:
        self.role = role
        if role == PlayerRole.IMPOSTOR:
            self.is_impostor = True
            # self.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
            self.state = RoundData(tasks=get_impostor_tasks())
            if self.adventure_agent: self.adventure_agent.role = PlayerRole.IMPOSTOR
            if self.discussion_agent: self.discussion_agent.role = PlayerRole.IMPOSTOR
            if self.voting_agent: self.voting_agent.role = PlayerRole.IMPOSTOR
        else:
            self.is_impostor = False
            self.kill_cooldown = 0
            if not self.state.tasks: self.state = RoundData(tasks=get_random_tasks())
            if self.adventure_agent: self.adventure_agent.role = PlayerRole.CREWMATE
            if self.discussion_agent: self.discussion_agent.role = PlayerRole.CREWMATE
            if self.voting_agent: self.voting_agent.role = PlayerRole.CREWMATE


    def set_stage(self, stage: GamePhase) -> None:
        self.state.stage = stage
        if stage == GamePhase.ACTION_PHASE:
            self.state.location = GameLocation.LOC_CAFETERIA

    def get_task_to_complete(self) -> List[Task]:
        return [task for task in self.state.tasks if not task.completed]

    def log_state_new_round(self) -> None:
        # Create a deep copy of the state before adding it to the history
        state_copy = copy.deepcopy(self.state)
        self.history.add_round(state_copy)
        # self.state.tasks = [task for task in self.state.tasks if not task.completed]
        self.state.llm_responses = []
        self.state.prompt = ""
        self.state.actions = []
        self.state.response = ""
        self.state.action_result = ""
        self.state.seen_actions = []
        self.state.player_in_room = ""
        # self.state.observations = [] # chat messages are here

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
        """
        :return: A string containing all the messages from the current round (observations with "chat" begginings)
        """
        return "\n".join([obs for obs in self.state.observations if obs.startswith("chat")])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def to_dict(self):
        agent_data = {}
        if self.adventure_agent:
            agent_data["adventure_agent"] = self.adventure_agent.to_dict()
        if self.discussion_agent:
            agent_data["discussion_agent"] = self.discussion_agent.to_dict()
        if self.voting_agent:
            agent_data["voting_agent"] = self.voting_agent.to_dict()

        return {
            "name": self.name,
            "role": self.role.value,
            "is_impostor": self.is_impostor,
            "kill_cooldown": self.kill_cooldown,
            "state": self.state.to_dict(),
            "history": self.history.to_dict(),
            "agents": agent_data,
        }
