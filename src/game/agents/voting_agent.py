from typing import List, Any
from .base_agent import Agent
from langchain.schema import HumanMessage
from llm_prompts import VOTING_TEMPLATE
import re

class VotingAgent(Agent):
    def update_state(self, observations: str, tasks: List[str] = None, actions: List[str] = None):
        self.state.history = observations
        self.state.available_actions = actions

    def choose_action(self, discussion_log: str) -> int:
        action_prompt = VOTING_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            discussion=discussion_log,
            history=self.state.history,
            actions="\n".join(
                f"{i+1}. {action}" for i, action in enumerate(self.state.available_actions)
            ),
        )
        chosen_action = self.llm.invoke([HumanMessage(content=action_prompt)])
        chosen_action_str = chosen_action.content.strip()
        self.responses.append(f"Chosen vote: {chosen_action_str}")
        vote = self.check_action_valid(chosen_action_str)
        return f"Vote prompt: {action_prompt}", vote

    def check_action_valid(self, chosen_action: str) -> int:
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in self.state.available_actions
        ]
        if normalized_chosen_action in normalized_available_actions:
            return normalized_available_actions.index(normalized_chosen_action)
        else:
            warning_str = f"{self.player_name} LLM did not conform to output format. Expected one of {normalized_available_actions}, but got {chosen_action} ({normalized_chosen_action} normalized)"
            print(warning_str)
            self.responses.append(warning_str)
            return 0 # Default to first action if invalid

    def act(self) -> Any:
        # choose_action is used
        return 0

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().lower()
