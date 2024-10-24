from typing import List, Any

from langchain_openai import ChatOpenAI

from game.consts import ASCII_MAP
from .base_agent import Agent
from langchain.schema import HumanMessage
from game.llm_prompts import ADVENTURE_PLAN_TEMPLATE, ADVENTURE_ACTION_TEMPLATE
import re


class AdventureAgent(Agent):
    llm: ChatOpenAI
    def update_state(
        self,
        observations: str,
        tasks: List[str],
        actions: List[str],
        current_location: str,
    ):
        self.state.history = observations
        self.state.current_tasks = tasks
        self.state.available_actions = actions
        self.state.current_location = current_location

    def create_plan(self) -> str:
        plan_prompt = ADVENTURE_PLAN_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            ASCII_MAP=ASCII_MAP,
            history=self.state.history,
            tasks=self.state.current_tasks,
            actions="<action>"
            + "</action><action>".join(self.state.available_actions)
            + "</action>",
            current_location=self.state.current_location,
        )
        plan = self.llm.invoke([HumanMessage(content=plan_prompt)])
        print(plan.usage_metadata)
        self.add_token_usage(plan.usage_metadata)
        return plan_prompt, plan.content.strip()

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
        self.add_token_usage(chosen_action.usage_metadata)
        chosen_action = chosen_action.content.strip()
        return action_prompt, self.check_action_valid(chosen_action)

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
            return 0

    def act(self) -> Any:
        plan_prompt, plan = self.create_plan()
        action_prompt, action = self.choose_action(plan)
        self.responses.append(
            f"Based on plan: {plan}\n{self.player_name} chose action: {action} {self.state.available_actions[action]}"
        )
        return f"Plan prompt:\n{plan_prompt}\n\nAction prompt:{action_prompt}", action

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().lower()
