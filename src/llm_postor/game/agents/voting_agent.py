import re
from typing import List, Any

from pydantic import Field
from .base_agent import Agent
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from llm_postor.game.llm_prompts import VOTING_TEMPLATE
from llm_postor.config import OPENROUTER_API_KEY
from llm_postor.game.agents.usage_metadata import UsageMetadata

class VotingAgent(Agent):
    llm: ChatOpenAI = None
    llm_model_name: str
    history: str = Field(default="")
    available_actions: List[str] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.init_llm()

    def init_llm(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("Missing OpenRouter API key. Please set OPENROUTER_API_KEY in your environment.")
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=self.llm_model_name,
            temperature=0
        )

    def act(
        self,
        observations: str,
        actions: List[str],
        discussion_log: str,
        dead_players: List[str],
    ) -> int:
        self.history = observations
        self.available_actions = actions

        action_prompt = VOTING_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            discussion=discussion_log,
            history=self.history,
            dead_players=dead_players,
            actions="\n".join(
                f"- {action}"
                for i, action in enumerate(self.available_actions)
            ),
        )
        # print("\nAction prompt voting:", action_prompt)
        chosen_action = self.llm.invoke([HumanMessage(content=action_prompt)])
        # print("\nVoted for:", chosen_action.content)
        self.add_token_usage(chosen_action.usage_metadata)
        chosen_action_str = chosen_action.content.strip()
        self.responses.append(chosen_action_str)
        vote = self.check_action_valid(chosen_action_str)
        return f"Vote prompt: {action_prompt}", vote

    def check_action_valid(self, chosen_action: str) -> int:
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in self.available_actions
        ]
        if normalized_chosen_action in normalized_available_actions:
            return normalized_available_actions.index(normalized_chosen_action)
        else:
            warning_str = f"{self.player_name} LLM did not conform to output format. Expected one of {normalized_available_actions}, but got {chosen_action} ({normalized_chosen_action} normalized)"
            print(warning_str)
            raise ValueError(warning_str)
            self.responses.append(warning_str)
            return 0  # Default to first action if invalid

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().strip(".").lower()
