from typing import List, Any
from .base_agent import Agent
from langchain.schema import HumanMessage
from llm_prompts import VOTING_TEMPLATE
import re

class VotingAgent(Agent):
    def update_state(self, observation: str, tasks: List[str] = None, actions: List[str] = None):
        self.state.history.append(observation)

    def choose_action(self, discussion_log: str, available_actions: List[str]) -> int:
        action_prompt = VOTING_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            discussion=discussion_log,
            history="\n".join(self.state.history),
            actions="\n".join(
                f"{i+1}. {action}" for i, action in enumerate(available_actions)
            ),
        )
        chosen_action = self.llm.invoke([HumanMessage(content=action_prompt)])
        self.responses.append(f"Chosen vote: {chosen_action.content.strip()}")
        chosen_action = chosen_action.content.strip()
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in available_actions
        ]
        if normalized_chosen_action not in normalized_available_actions:
            return 0  # Default to first action if invalid
        return normalized_available_actions.index(normalized_chosen_action)

    def act(self) -> Any:
        # This method should be called with the necessary arguments
        # For now, we'll return a placeholder value
        return 0

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().lower()
