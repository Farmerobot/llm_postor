from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel, Field

from llm_postor.game.agents.usage_metadata import UsageMetadata
from llm_postor.game.consts import TOKEN_COSTS

class AgentState(BaseModel):
    history: str = Field(default_factory=str)
    current_tasks: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)
    messages: List[str] = Field(default_factory=list)
    current_location: str = Field(default_factory=str)
    token_usage: UsageMetadata = Field(default_factory=UsageMetadata)

    def to_dict(self):
        return {
            "history": self.history,
            "current_tasks": self.current_tasks,
            "available_actions": self.available_actions,
            "messages": self.messages,
            "current_location": self.current_location,
            "token_usage": self.token_usage.to_dict(),
        }


class Agent(ABC, BaseModel):
    # has to be Any because of MagicMock. TODO: Fix test integration with pydanitc
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
    
    def add_token_usage(self, msg: dict):
        # {'input_tokens': 998, 'output_tokens': 82, 'total_tokens': 1080, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}
        self.state.token_usage.input_tokens += msg["input_tokens"]
        self.state.token_usage.output_tokens += msg["output_tokens"]
        self.state.token_usage.total_tokens += msg["total_tokens"]
        if "cache_read" in msg["input_token_details"]:
            self.state.token_usage.cache_read += msg["input_token_details"]["cache_read"]
        self.update_cost()
        
    def update_cost(self):
        for_model = self.llm.model_name
        if for_model not in TOKEN_COSTS:
            print(f"Model {for_model} not found in TOKEN_COSTS. defaulting to openai/gpt-4o-mini")
            for_model = "openai/gpt-4o-mini"
        
        self.state.token_usage.cost += self.state.token_usage.input_tokens * TOKEN_COSTS[for_model]["input_tokens"] 
        self.state.token_usage.cost += self.state.token_usage.output_tokens * TOKEN_COSTS[for_model]["output_tokens"]
        self.state.token_usage.cost += self.state.token_usage.cache_read * TOKEN_COSTS[for_model]["cache_read"]
        

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
