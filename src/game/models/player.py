from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Any, Union

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from collections import OrderedDict

from game.agents.adventure_agent import AdventureGameAgent
from game.agents.discussion_agent import DiscussionAgent
from game.agents.voting_agent import VotingAgent
from game.models.game_models import (
    HUMAN_READABLE_LOCATIONS,
    GamePhase,
    PlayerRole,
    PlayerState,
    GameLocation,
    Task,
)
import game.consts as game_consts

class Player(ABC):
    def __init__(
        self,
        name: str,
        role: PlayerRole = PlayerRole.CREWMATE,
    ):
        self.name = name
        self.role = role
        self.player_stage = GamePhase.MAIN_MENU
        self.player_state = PlayerState.ALIVE
        self.player_location = GameLocation.LOC_CAFETERIA
        self.player_tasks: List[Task] = []
        self.can_vote = False
        self.is_impostor = False
        self.kill_cooldown = 0
        self.history: List[OrderedDict] = []  # observation and action history
        self.responses: List[str] = []
        self.chat_history: List = []
        self.prev_location: Optional[GameLocation] = None
        self.discussion_prompt: str = ""
        self.set_role(role)

    def set_role(self, role: PlayerRole) -> None:
        self.role = role
        if role == PlayerRole.IMPOSTOR:
            self.is_impostor = True
            self.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
        else:
            self.is_impostor = False

    def set_state(self, state: PlayerState) -> None:
        self.player_state = state

    def set_location(self, location: GameLocation) -> None:
        self.player_location = location

    def get_location(self) -> GameLocation:
        return self.player_location

    def set_stage(self, stage: GamePhase) -> None:
        self.player_stage = stage
        if stage == GamePhase.DISCUSS:
            self.can_vote = True
        if stage == GamePhase.ACTION_PHASE:
            self.can_vote = False
            self.player_location = GameLocation.LOC_CAFETERIA

    def set_tasks(self, tasks: List[Task]) -> None:
        self.player_tasks = tasks

    def get_task_to_complete(self) -> List[Task]:
        return [task for task in self.player_tasks if not task.completed]

    @abstractmethod
    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        pass

    @abstractmethod
    def prompt_discussion(self) -> str:
        pass

    @abstractmethod
    def prompt_vote(self, voting_actions: List[str]) -> int:
        pass

    def get_message_str(self) -> str:
        return "\n".join(self.chat_history[-1])

    def get_history_str(self) -> str:
        history = ""
        for key, val in self.history[-1].items():
            if isinstance(val, str):
                history += f"{val}\n"
            if isinstance(val, list):
                if len(val) > 1:
                    history += "\n".join(val) + "\n"

        return history

    def get_obervation_history(self) -> str:
        history = ""
        acceptable_keys = [
            "action_result",
            "seen_action",
            "current_location",
            "player_in_room",
        ]
        for round in self.history:
            for key, val in round.items():
                if key not in acceptable_keys:
                    continue
                if isinstance(val, str):
                    history += f"{val}\n"
                if isinstance(val, list):
                    if len(val) > 1:
                        history += "\n".join(val) + "\n"
                    else:
                        history += f"{val[0]}\n"
        return history

    def turns_passed(self) -> int:
        return len(self.history)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class HumanPlayer(Player):
    def __init__(self, name: str, role: PlayerRole = PlayerRole.CREWMATE):
        super().__init__(name, role)
        self.adventure_agent = None
        self.discussion_agent = None
        self.voting_agent = None

    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        task_str = "\n".join([str(task) for task in self.player_tasks])
        self.history[-1]["story"] = f"Your turn {self.name}: {prompt}"
        action_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(actions)]
        )
        self.history[-1]["actions"] = action_prompt

        print("========================================")
        self.history[-1]["tasks"] = f"Here are your tasks: \n{task_str}"
        print(self.get_history_str())

        while True:
            try:
                choosen_action = int(input("Choose action (enter the number): "))
                if 0 <= choosen_action < len(actions):
                    self.history[-1]["action"] = actions[choosen_action]
                    return choosen_action
                else:
                    print(f"Please enter a number between 0 and {len(actions) - 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")
            self.history[-1]["error"] = "Invalid action"

    def prompt_discussion(self) -> str:
        self.history[-1]["observations"] = self.get_obervation_history()
        self.history[-1].move_to_end("observations", last=False)
        history = self.get_history_str()
        messages = self.get_message_str()
        print(history)
        print(messages)
        print(f"{self.name} it's your turn to discuss")
        answer = input("")
        return answer

    def prompt_vote(self, voting_actions: List[str]) -> int:
        voting_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(voting_actions)]
        )
        self.history[-1]["voting"] = voting_prompt
        print(self.get_history_str())
        answer = input("Choose player to banish: ")
        if answer.isdigit():
            return int(answer)
        else:
            return self.prompt_vote(voting_actions)


class AIPlayer(Player):
    def __init__(self, name: str, model_name: str, role: PlayerRole = PlayerRole.CREWMATE):
        super().__init__(name, role)
        if model_name.startswith("gpt"):
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.1,
            )
        elif model_name.startswith("gemini"):
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.1,
            )
        self.adventure_agent = AdventureGameAgent(llm=self.llm, player_name=self.name)
        self.discussion_agent = DiscussionAgent(llm=self.llm, player_name=self.name)
        self.voting_agent = VotingAgent(llm=self.llm, player_name=self.name)

        role_str = "crewmate" if role == PlayerRole.CREWMATE else "impostor"
        self.adventure_agent.role = role_str
        self.discussion_agent.role = role_str
        self.voting_agent.role = role_str

    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        self.adventure_agent.update_state(
            observation=self.get_history_str(),
            tasks=self.get_task_to_complete(),
            actions=actions,
            current_location=HUMAN_READABLE_LOCATIONS[self.get_location()],
        )
        return self.adventure_agent.act()

    def prompt_discussion(self) -> str:
        self.history[-1]["observations"] = self.get_obervation_history()
        self.history[-1].move_to_end("observations", last=False)
        history = self.get_history_str()
        statements = self.get_message_str()
        self.discussion_agent.update_state(observation=history, messages=statements)
        points = self.discussion_agent.create_discussion_points(statements=statements)
        return self.discussion_agent.act(points)

    def prompt_vote(self, voting_actions: List[str]) -> int:
        self.voting_agent.update_state(observation=self.get_obervation_history())
        return self.voting_agent.choose_action(self.get_message_str(), voting_actions)
