from typing import List, Any

from game.consts import ASCII_MAP
from .base_agent import Agent, GameState
from langchain.schema import HumanMessage
from llm_prompts import ADVENTURE_PLAN_TEMPLATE, ADVENTURE_ACTION_TEMPLATE
import re

class AdventureAgent(Agent):
    def update_state(self, observation: str, tasks: List[str], actions: List[str], current_location: str):
        self.state.history.append(observation)
        self.state.current_tasks = tasks
        self.state.available_actions = actions
        self.state.current_location = current_location

    def create_plan(self) -> str:
        plan_prompt = ADVENTURE_PLAN_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            ASCII_MAP=ASCII_MAP,
            history="\n".join(self.state.history),
            tasks=self.state.current_tasks,
            actions="<action>"+"</action><action>".join(self.state.available_actions)+"</action>",
            current_location=self.state.current_location,
        )
        plan = self.llm.invoke([HumanMessage(content=plan_prompt)])
        return plan.content.strip()

    def choose_action(self, plan: str) -> int:
        action_prompt = ADVENTURE_ACTION_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history),
            task=self.state.current_tasks,
            actions=", ".join(self.state.available_actions),
            plan=plan,
        )
        chosen_action = self.llm.invoke([HumanMessage(content=action_prompt)])
        chosen_action = chosen_action.content.strip()
        self.responses.append(f"From these actions: {self.state.available_actions}")
        self.responses.append(f"Chosen action: {chosen_action}")
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in self.state.available_actions
        ]
        if normalized_chosen_action not in normalized_available_actions:
            return 0  # Default to first action if invalid
        return normalized_available_actions.index(normalized_chosen_action)

    def act(self) -> Any:
        plan = self.create_plan()
        action = self.choose_action(plan)
        self.responses.append(f"{self.player_name} chose action: {action} based on plan: {plan}")
        return action

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().lower()
