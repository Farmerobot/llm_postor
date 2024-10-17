from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel, Field, ConfigDict

class GameState(BaseModel):
    history: List[str] = Field(default_factory=list)
    current_tasks: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)

class Agent(ABC, BaseModel):
    llm: Any
    state: GameState = Field(default_factory=GameState)
    responses: List[str] = Field(default_factory=list)
    player_name: str = ""
    role: str = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def update_state(self, observation: str, tasks: List[str] = None, actions: List[str] = None):
        pass

    @abstractmethod
    def act(self) -> Any:
        pass
