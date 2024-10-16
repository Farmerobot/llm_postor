from game.models.game_models import (
    GamePhase,
    PlayerRole,
    PlayerState,
    GameLocation,
    Task,
)
from typing import Union
from enum import Enum
from typing import Optional, Any
from random import choice
from game import consts
from collections import OrderedDict
from langchain_openai import ChatOpenAI
from game.agents.AdventureAgent import AdventureGameAgent
from game.agents.DiscussionAgent import DiscussionAgent
from game.agents.VotingAgent import VotingAgent
import game.consts as game_consts


class Player:
    def __init__(
        self,
        name: str,
        agent: str = "human",
        model_name: str = "",
        role: PlayerRole = PlayerRole.CREWMATE,
    ):
        self.name: str = name
        self.player_stage: GamePhase = GamePhase.MAIN_MENU
        self.player_state: PlayerState = PlayerState.ALIVE
        self.player_location: GameLocation = GameLocation.LOC_CAFETERIA
        self.player_tasks: list[Task] = []
        self.can_vote: bool = False
        self.is_impostor: bool = False
        self.kill_cooldown: int = 0
        self.history: list[OrderedDict] = []  # observation and action history
        self.chat_history: list = []
        self.prev_location: Optional[GameLocation] = None
        self.discussion_prompt: str = ""

        assert agent in ["human", "random", "ai"]
        self.agent = agent
        if agent == "ai":
            if model_name.startswith("gpt"):
                self.llm = ChatOpenAI(
                    model=model_name,
                    temperature=0.1,
                )
        self.set_role(role)

    def set_role(self, role: PlayerRole) -> None:
        self.player_role = role
        if role == PlayerRole.IMPOSTOR:
            self.is_impostor = True
            self.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
        else:
            self.is_impostor = False

        if self.agent == "ai":
            role_str = "crewmate" if role == PlayerRole.CREWMATE else "impostor"
            self.adventure_agent = AdventureGameAgent(
                llm=self.llm, player_name=self.name
            )
            self.discussion_agent = DiscussionAgent(
                llm=self.llm, player_name=self.name, role=role_str
            )
            self.voting_agent = VotingAgent(
                llm=self.llm, player_name=self.name, role=role_str
            )

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

    def set_tasks(self, tasks: list[Task]) -> None:
        self.player_tasks = tasks

    def get_task_to_complete(self) -> list[Task]:
        return [task for task in self.player_tasks if not task.completed]

    def prompt_action(self, prompt: str, actions: list[str]) -> int:
        task_str = "\n".join([str(task) for task in self.player_tasks])
        self.history[-1]["story"] = f"Your turn {self.name}: {prompt}"
        action_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(actions)]
        )
        self.history[-1]["actions"] = action_prompt
        if self.agent == "human":
            print("========================================")
            self.history[-1]["tasks"] = f"Here are your tasks: \n{task_str}"
            print(self.get_history_str())
            try:
                choosen_action = int(input("Choose action: "))
            except ValueError:
                self.history[-1]["error"] = "Invalid action"
                return self.prompt_action(prompt, actions)
            if not 0 <= choosen_action < len(actions):
                self.history[-1]["error"] = "Invalid action"
                return self.prompt_action(prompt, actions)
            return choosen_action
        if self.agent == "random":
            return choice(range(len(actions)))
        if self.agent == "ai":
            history = self.get_history_str()
            tasks = self.get_task_to_complete()
            tasks_str = [task.name for task in tasks]
            self.adventure_agent.update_state(
                observation=history, tasks=tasks_str, actions=actions
            )
            return self.adventure_agent.act()

        self.history.append(OrderedDict())
        return 0

    def prompt_discussion(self) -> str:
        self.history[-1]["observations"] = self.get_obervation_history()
        self.history[-1].move_to_end("observations", last=False)
        history = self.get_history_str()
        messages = self.get_message_str()
        if self.agent == "human":
            print(history)
            print(messages)
            print(f"{self.name} it's your turn to discuss")
            answer = input("")
        if self.agent == "random":
            answer = ""
        if self.agent == "ai":
            if self.discussion_prompt == "":
                self.discussion_agent.update_state(
                    observation=history,
                )
                self.discussion_prompt = (
                    self.discussion_agent.create_discussion_points()
                )
            answer = self.discussion_agent.respond_to_statements(messages)
        return answer

    def prompt_vote(self, voting_actions: list[str]) -> int:
        voting_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(voting_actions)]
        )
        self.history[-1]["voting"] = voting_prompt
        if self.agent == "human":
            print(self.get_history_str())
            answer = input("Choose player to banish: ")
            if answer.isdigit():
                return int(answer)
            else:
                return self.prompt_vote(voting_actions)
        if self.agent == "random":
            return choice(range(len(voting_actions)))
        if self.agent == "ai":
            self.voting_agent.update_state(
                observation=self.get_obervation_history(),
            )
            return self.voting_agent.choose_action(
                self.get_message_str(), voting_actions
            )
        return 0

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


class GameActionType(Enum):
    VOTE = -1
    WAIT = 0
    MOVE = 1
    DO_ACTION = 2
    KILL = 3
    REPORT = 4

    def __lt__(self, other):
        if isinstance(other, GameActionType):
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, GameActionType):
            return self.value > other.value
        return NotImplemented


class GameAction:
    def __init__(
        self,
        action: GameActionType,
        source: Player,
        target: Optional[Union[Player, GameLocation, Task, list]] = None,
    ):
        self.action_type: GameActionType = action
        self.source = source
        self.target = target
        self.location = source.get_location()
        self.input_stories = {
            GameActionType.MOVE: f"move to location {self.target}",
            GameActionType.WAIT: f"wait in {self.location}",
            GameActionType.DO_ACTION: f"complete task: {self.target.name if isinstance(self.target, Task) else self.target}",
            GameActionType.REPORT: f"report dead body of {str(self.target)}",
            GameActionType.KILL: f"kill {str(self.target)}",
            GameActionType.VOTE: f"vote for {str(self.target)}",
        }
        self.output_stories = {
            GameActionType.MOVE: f"You [{self.source}] moved to {self.target}",
            GameActionType.WAIT: f"You [{self.source}] are waiting in {self.location}",
            GameActionType.DO_ACTION: f"You[{self.source}]  {self.target}",
            GameActionType.REPORT: f"You [{self.source}] reported {str(self.target)}",
            GameActionType.KILL: f"You [{self.source}] killed {str(self.target)}",
            GameActionType.VOTE: f"You [{self.source}] voted for {str(self.target)}",
        }
        self.spectator_stories = {
            GameActionType.MOVE: f"{self.source} moved to {self.target} from {self.location}",
            GameActionType.WAIT: f"{self.source} waited",
            GameActionType.DO_ACTION: f"{self.source} doing task",
            GameActionType.REPORT: f"{self.source} reported dead body of {self.target}",
            GameActionType.KILL: f"{self.source} killed {self.target}",
            GameActionType.VOTE: f"{self.source} voted for {self.target}",
        }

    def get_input_story(self):
        return self.input_stories[self.action_type]

    def get_output_story(self):
        return self.output_stories[self.action_type]

    def get_spectator_story(self):
        return self.spectator_stories[self.action_type]

    def do_action(self):
        if (
            self.action_type == GameActionType.REPORT
            or self.action_type == GameActionType.WAIT
        ):
            pass
        if self.action_type == GameActionType.MOVE:
            self.source.set_location(self.target)
        if self.action_type == GameActionType.DO_ACTION:
            return self.target.complete(self.target.location)
        if self.action_type == GameActionType.KILL:
            self.target.set_state(PlayerState.DEAD)
            self.source.kill_cooldown = game_consts.IMPOSTOR_COOLDOWN
        return self.get_output_story()

    def __str__(self):
        return f"{self.action_type} | {self.target}"

    def __repr__(self):
        return f"{self.action_type} | {self.target}"
