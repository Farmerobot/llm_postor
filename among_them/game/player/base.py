import copy
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, ClassVar, List, Optional, Self

from pydantic import BaseModel, ConfigDict, Field

from among_them.game.behavior.base import Behavior
import among_them.game.consts as game_consts
from among_them.game.agents.adventure_agent import AdventureAgent
from among_them.game.agents.discussion_agent import DiscussionAgent
from among_them.game.agents.voting_agent import VotingAgent
from among_them.game.models.engine import (
    GameLocation,
    GamePhase,
)
from among_them.game.models.history import PlayerHistory, RoundData
from among_them.game.models.tasks import Task
from among_them.game.scene import Location
from among_them.game.utils import get_impostor_tasks, get_random_tasks


class Player(BaseModel, ABC):
    _players: ClassVar[dict[str, type[Self]]]
    TYPE: ClassVar[str]

    name: str
    alive: bool
    behavior: Behavior | None = None
    tasks: list[Task] | None = None
    state: RoundData | None
    history: PlayerHistory | None = None

    @classmethod
    def dispatch(cls, model: dict) -> Self:
        return cls._players[model["TYPE"]].model_validate(model)


    def log_state_new_round(self, prev_round_game_stage) -> None:
        # Before creating new state, update the game_stage in each players' history
        self.state.stage = prev_round_game_stage
        # Create a deep copy of the state before adding it to the history
        state_copy = copy.deepcopy(self.state)
        self.history.add_round(state_copy)
        # self.state.tasks = [task for task in self.state.tasks if not task.completed]
        self.state.llm_responses = []
        self.state.prompts = []
        self.state.actions = []
        self.state.response = ""
        self.state.action_result = ""
        self.state.seen_actions = []
        self.state.player_in_room = ""
        self.state.observations = []
        # self.state.chat_messages = []

    @abstractmethod
    def prompt_action(self, actions: List[str]) -> int:
        pass

    @abstractmethod
    def prompt_discussion(self) -> str:
        pass

    @abstractmethod
    def prompt_vote(self, voting_actions: List[str], dead_players: List[str]) -> int:
        pass

    def get_chat_messages(self) -> List[str]:
        """
        :return: A string containing all the messages from the current round (observations with "chat" begginings)
        """
        return [obs[18:] for obs in self.state.chat_messages if obs.startswith("chat")]
