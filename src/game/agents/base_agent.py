from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel, Field, ConfigDict

class AgentState(BaseModel):
    history: str = Field(default_factory=str)
    current_tasks: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)
    messages: List[str] = Field(default_factory=list)
    current_location: str = Field(default_factory=str)

class Agent(ABC, BaseModel):
    llm: Any
    state: AgentState = Field(default_factory=AgentState)
    responses: List[str] = Field(default_factory=list)
    player_name: str = ""
    role: str = ""

    @abstractmethod
    def update_state(self, observations: str, tasks: List[str] = None, actions: List[str] = None):
        pass

    @abstractmethod
    def act(self) -> Any:
        pass
