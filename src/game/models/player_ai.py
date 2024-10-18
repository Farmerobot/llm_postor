from typing import List, Optional

from game.agents.adventure_agent import AdventureAgent
from game.agents.discussion_agent import DiscussionAgent
from game.agents.voting_agent import VotingAgent
from game.models.player import Player, PlayerRole
from game.models.game_models import HUMAN_READABLE_LOCATIONS

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class AIPlayer(Player):
    llm_model_name: str
    llm: Optional[ChatOpenAI | ChatGoogleGenerativeAI] = None
    model_config = Player.model_config

    def __init__(self, **data):
        super().__init__(**data)  # Initialize Player fields first
        if self.llm_model_name.startswith("gpt"):
            self.llm = ChatOpenAI(model=self.llm_model_name,temperature=0.1)
        elif self.llm_model_name.startswith("gemini"):
            self.llm = ChatGoogleGenerativeAI(
                model=self.llm_model_name,
                temperature=0.1,
            )
        self.adventure_agent = AdventureAgent(llm=self.llm, player_name=self.name)
        self.discussion_agent = DiscussionAgent(llm=self.llm, player_name=self.name)
        self.voting_agent = VotingAgent(llm=self.llm, player_name=self.name)

        role_str = "crewmate" if self.role == PlayerRole.CREWMATE else "impostor"
        self.adventure_agent.role = role_str
        self.discussion_agent.role = role_str
        self.voting_agent.role = role_str

    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        self.adventure_agent.update_state(
            observation=self.history.get_history_str(),
            tasks=self.get_task_to_complete(),
            actions=actions,
            current_location=HUMAN_READABLE_LOCATIONS[self.location],
        )
        return self.adventure_agent.act()

    def prompt_discussion(self) -> str:
        self.history[-1]["observations"] = self.get_observation_history()
        self.history[-1].move_to_end("observations", last=False)
        history = self.get_history_str()
        statements = self.get_message_str()
        self.discussion_agent.update_state(observation=history, messages=statements)
        points = self.discussion_agent.create_discussion_points(statements=statements)
        return self.discussion_agent.act(points)

    def prompt_vote(self, voting_actions: List[str]) -> int:
        self.voting_agent.update_state(observation=self.get_observation_history())
        return self.voting_agent.choose_action(self.get_message_str(), voting_actions)

