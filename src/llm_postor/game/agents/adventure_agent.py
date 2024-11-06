import re
from typing import List, Any
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from llm_postor.game.agents.base_agent import Agent
from llm_postor.game.consts import ASCII_MAP
from llm_postor.game.llm_prompts import ADVENTURE_PLAN_TEMPLATE, ADVENTURE_ACTION_TEMPLATE
from llm_postor.config import OPENROUTER_API_KEY

class AdventureAgent(Agent):
    llm: ChatOpenAI = None
    response_llm: ChatOpenAI = None
    llm_model_name: str

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
            temperature=1
        )
        self.response_llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=self.llm_model_name,
            temperature=0
        )

    def update_state(
        self,
        observations: str,
        tasks: List[str],
        actions: List[str],
        current_location: str,
        in_room: str,
    ):
        self.state.history = observations
        self.state.current_tasks = tasks
        self.state.available_actions = actions
        self.state.current_location = current_location
        self.state.in_room = in_room

    def create_plan(self) -> str:
        plan_prompt = ADVENTURE_PLAN_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history=self.state.history,
            tasks=[str(task) for task in self.state.current_tasks],
            actions="- " + "\n- ".join(self.state.available_actions),
            in_room=self.state.in_room,
            current_location=self.state.current_location,
        )
        # print("\nPlan prompt:", plan_prompt)
        plan = self.llm.invoke([HumanMessage(content=plan_prompt)])
        # print("\nCreated plan:", plan.content)
        self.add_token_usage(plan.usage_metadata)
        return plan_prompt, plan.content.strip()

    def choose_action(self, plan: str) -> int:
        action_prompt = ADVENTURE_ACTION_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history),
            task=self.state.current_tasks,
            actions="- " + "\n- ".join(self.state.available_actions),
            plan=plan,
        )
        # print("\nAction prompt", action_prompt)
        chosen_action = self.response_llm.invoke([HumanMessage(content=action_prompt)])
        # print("\nChosen action:", chosen_action.content)
        self.add_token_usage(chosen_action.usage_metadata)
        chosen_action = chosen_action.content.strip()
        return action_prompt, *self.check_action_valid(chosen_action)

    def check_action_valid(self, chosen_action: str) -> int:
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in self.state.available_actions
        ]
        if normalized_chosen_action in normalized_available_actions:
            return normalized_available_actions.index(normalized_chosen_action), normalized_chosen_action
        else:
            warning_str = f"{self.player_name} LLM did not conform to output format. Expected one of {normalized_available_actions}, but got '{chosen_action}'"
            print(warning_str)
            raise ValueError(warning_str)
            self.responses.append(warning_str)
            return 0

    def act(self) -> Any:
        plan_prompt, plan = self.create_plan()
        action_prompt, action_idx, action = self.choose_action(plan)
        self.responses.append(plan)
        self.responses.append(action)
        return f"Plan prompt:\n{plan_prompt}\n\nAction prompt:{action_prompt}", action_idx

    @staticmethod
    def normalize_action(action: str) -> str:
        return re.sub(r"^\d+[\s:.)-]*", "", action).strip().strip(".").lower()
