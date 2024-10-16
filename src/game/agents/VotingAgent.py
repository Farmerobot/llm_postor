import pydantic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Any, List
import re
import datetime


class GameState(BaseModel):
    history: list[str] = Field(default_factory=list)


class VotingAgent(BaseModel):
    llm: Any
    state: GameState = Field(default_factory=GameState)
    player_name: str = ""
    role: str = ""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    def update_state(self, observation: str):
        self.state.history.append(observation)

    def choose_action(self, discussion_log: str, available_actions: List[str]) -> int:
        action_template = """
        You are {player_name}, a player in an Among Us-like game. It's time to vote on who to eject from the game.
        You are {player_role}.

        Game history and your observations:
        {history}
        Discusssion messages:
        {discussion}

        Available voting actions:
        {actions}

        Based on the game history and your observations, choose the best action to take.
        If you're an impostor, try to avoid suspicion and protect your team.
        If you're a crewmate, try to identify the most suspicious player based on the available information.

        Your response should be exactly one of the available actions.

        Chosen action:
        """

        action_prompt = action_template.format(
            player_name=self.player_name,
            player_role=self.role,
            discussion=discussion_log,
            history="\n".join(self.state.history),
            actions="\n".join(
                f"{i+1}. {action}" for i, action in enumerate(available_actions)
            ),
        )

        chosen_action = self.llm.predict(action_prompt)
        chosen_action = chosen_action.strip()

        # Ensure the chosen action is one of the available actions
        normalized_chosen_action = self.normalize_action(chosen_action)
        normalized_available_actions = [
            self.normalize_action(action) for action in available_actions
        ]

        if normalized_chosen_action not in normalized_available_actions:
            return 0  # Default to first action if invalid
        # print(f"Chosen action: {chosen_action}")
        # save_path = f"chosen_action_{self.player_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        # with open(save_path, "w") as f:
        #     f.write(f"Chosen action: {chosen_action}")
        return normalized_available_actions.index(normalized_chosen_action)

    def normalize_action(self, action: str) -> str:
        # Remove any leading numbers or punctuation
        action = re.sub(r"^\d+[\s:.)-]*", "", action).strip()
        return action.lower()


# Example usage:
# llm = ChatOpenAI(temperature=0.7)
# game_state = GameState()
# agent = VotingAgent(llm=llm, state=game_state, player_name="Red")
# agent.update_state("Red saw Blue in Electrical")
# available_actions = ["Vote to eject Blue", "Vote to eject Green", "Vote to eject Yellow", "Skip Vote"]
# action_index = agent.choose_action(available_actions)
# chosen_action = available_actions[action_index]
