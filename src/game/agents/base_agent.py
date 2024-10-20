from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    history: str = Field(default_factory=str)
    current_tasks: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)
    messages: List[str] = Field(default_factory=list)
    current_location: str = Field(default_factory=str)

    def to_dict(self):
        return {
            "history": self.history,
            "current_tasks": self.current_tasks,
            "available_actions": self.available_actions,
            "messages": self.messages,
            "current_location": self.current_location,
        }


class Agent(ABC, BaseModel):
    # has to be Any because of MagicMock. TODO: Fix test integration with pydanitc
    llm: Any  # Optional[ChatOpenAI | ChatGoogleGenerativeAI] = None
    state: AgentState = Field(default_factory=AgentState)
    responses: List[str] = Field(default_factory=list)
    player_name: str = ""
    role: str = ""

    @abstractmethod
    def update_state(
        self, observations: str, tasks: List[str] = None, actions: List[str] = None
    ):
        pass

    @abstractmethod
    def act(self) -> Any:
        pass

    def to_dict(self):
        llm_data = "human"
        if self.llm:
            if hasattr(self.llm, "model_name"):
                llm_data = self.llm.model_name
            elif hasattr(self.llm, "model"):
                llm_data = self.llm.model
            else:
                llm_data = "unknown"

        return {
            "llm": llm_data,
            "state": self.state.to_dict(),
            "responses": self.responses,
            "player_name": self.player_name,
            "role": self.role,
        }
