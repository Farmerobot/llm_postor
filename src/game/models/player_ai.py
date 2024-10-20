from typing import List, Optional
from pydantic import Field

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

    def __init__(self, **data):
        super().__init__(**data)  # Initialize Player fields first
        if self.llm_model_name.startswith("gpt"):
            self.llm = ChatOpenAI(model=self.llm_model_name,temperature=0.1)
        elif self.llm_model_name.startswith("gemini"):
            self.llm = ChatGoogleGenerativeAI(
                model=self.llm_model_name,
                temperature=0.1,
            )
        role_str = "crewmate" if self.role == PlayerRole.CREWMATE else "impostor"
        self.adventure_agent = AdventureAgent(llm=self.llm, player_name=self.name, role=role_str)
        self.discussion_agent = DiscussionAgent(llm=self.llm, player_name=self.name, role=role_str)
        self.voting_agent = VotingAgent(llm=self.llm, player_name=self.name, role=role_str)

    def prompt_action(self, actions: List[str]) -> int:
        self.state.actions = actions
        self.adventure_agent.update_state(
            observations=self.history.get_history_str(),
            tasks=self.get_task_to_complete(),
            actions=actions,
            current_location=HUMAN_READABLE_LOCATIONS[self.state.location],
        )
        prompts, chosen_action = self.adventure_agent.act()
        self.state.llm_responses = self.adventure_agent.responses
        self.state.response = chosen_action
        self.state.prompt = prompts
        return chosen_action

    def prompt_discussion(self) -> str:
        history = self.history.get_history_str()
        statements = self.get_message_str()
        self.discussion_agent.update_state(observations=history, messages=statements)
        message_prompt, message = self.discussion_agent.act()
        self.state.llm_responses = self.discussion_agent.responses
        self.state.response = message
        self.state.prompt = message_prompt
        return message

    def prompt_vote(self, voting_actions: List[str]) -> int:
        self.state.actions = voting_actions
        self.voting_agent.update_state(observation=self.history.get_history_str(), actions=voting_actions)
        vote_prompt, vote = self.voting_agent.choose_action(self.get_message_str())
        self.state.llm_responses = self.voting_agent.responses
        self.state.response = vote
        self.state.prompt = vote_prompt
        return vote

