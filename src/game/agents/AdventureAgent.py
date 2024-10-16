import pydantic
from langchain_openai import ChatOpenAI
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from typing import Any
from pydantic import BaseModel, Field, ConfigDict
import re
import datetime

# You need to set your OpenAI API key as an environment variable
# or pass it directly to the OpenAI constructor


class GameState(BaseModel):
    history: list[str] = Field(default_factory=list)
    current_tasks: list[str] = [""]
    available_actions: list[str] = Field(default_factory=list)


class AdventureGameAgent(BaseModel):
    llm: Any
    state: GameState = Field(default_factory=GameState)
    player_name: str = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def update_state(self, observation: str, tasks: list[str], actions: list[str]):
        self.state.history.append(observation)
        self.state.current_tasks = tasks
        self.state.available_actions = actions

    def create_plan(self) -> str:
        plan_template = """
        You are a game agent with the following state:
        
        History of observations:
        {history}
        
        Current tasks: 
        {tasks}
        ASCII map of the game:
            |\\----------------|--------------|----------------|--------------\\
            |                                                                 \\
            | UPPER ENGINE                        CAFETERIA       WEAPONS      \\
            |                 |-     --------|                |                 \\
            |/--------|    |--|       MEDBAY |                |                  \\
                    |    |                 |                |                   \\------\\
            /---------|    |-------\\         |                |----------|        |       \\
            |         |    |        \\        |---|     |------|          |                 |
            |                        \\       |                |                            |
            | REACTOR        SECURITY |      |  ADMIN OFFICE  |   O2           NAVIGATION  |
            |                         |      |                |          |                 |
            |         |    |          |      |---|     |----|-|----------|                 |
            \\---------|    |----------|------|              |                     |       /
                    |    |                 |                                    /------/
            |\\--------|    |--|              |                                   /
            |                 |              |              |--    --|          /
            | LOWER ENGINE       ELECTRICAL       STORAGE   | COMMS  | SHIELDS /
            |                                               |        |        /
            |/----------------|--------------|--------------|--------|-------/
        
        Available actions: {actions}
        
        Based on this information, create a plan to accomplish the current task.
        Your plan should be a step-by-step approach, considering your past observations.
        
        Plan:
        """

        plan_prompt = plan_template.format(
            history="\n".join(self.state.history),
            tasks=self.state.current_tasks,
            actions=", ".join(self.state.available_actions),
        )

        plan = self.llm.predict(plan_prompt)
        return plan.strip()

    def choose_action(self, plan: str) -> int:
        action_template = """
        You are a game agent with the following state:
        
        History of observations:
        {history}
        
        Current task: {task}
        
        Available actions: {actions}
        
        You have created the following plan:
        {plan}
        
        Based on your plan and the available actions, choose the best action to take next.
        Your response should be exactly one of the available actions.
        
        Chosen action:
        """

        action_prompt = action_template.format(
            history="\n".join(self.state.history),
            task=self.state.current_tasks,
            actions=", ".join(self.state.available_actions),
            plan=plan,
        )

        chosen_action = self.llm.predict(action_prompt)
        chosen_action = chosen_action.strip()

        # Ensure the chosen action is one of the available actions
        normalized_chosen_action = normalize_action(chosen_action)
        normalized_available_actions = [
            normalize_action(action) for action in self.state.available_actions
        ]

        if normalized_chosen_action not in normalized_available_actions:
            return 0  # Default to first action if invalid

        return normalized_available_actions.index(normalized_chosen_action)

    def act(self) -> int:
        plan = self.create_plan()
        action = self.choose_action(plan)
        # save the plan and action to file
        # save_path = f"plan_and_action_{self.player_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        # with open(save_path, "w") as f:
        #     f.write(f"Plan:\n{plan}\n\nAction: {action}")
        return action


def normalize_action(action: str) -> str:
    # Remove any leading numbers or punctuation
    action = re.sub(r"^\d+[\s:.)-]*", "", action).strip()
    return action.lower()
