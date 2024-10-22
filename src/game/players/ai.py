from typing import List

from game.agents.adventure_agent import AdventureAgent
from game.agents.discussion_agent import DiscussionAgent
from game.agents.voting_agent import VotingAgent
from game.players.base_player import Player, PlayerRole

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class AIPlayer(Player):
    llm_model_name: str

    def __init__(self, **data):
        super().__init__(**data)  # Initialize Player fields first
        self.init_agents()
        
    def init_agents(self):
        llm = None
        if self.llm_model_name.startswith("gpt"):
            llm = ChatOpenAI(model=self.llm_model_name, temperature=0.1)
        elif self.llm_model_name.startswith("gemini"):
            llm = ChatGoogleGenerativeAI(
                model=self.llm_model_name,
                temperature=0.1,
            )
        role_str = self.role.value
        self.adventure_agent = AdventureAgent(
            llm=llm, player_name=self.name, role=role_str
        )
        self.discussion_agent = DiscussionAgent(
            llm=llm, player_name=self.name, role=role_str
        )
        self.voting_agent = VotingAgent(llm=llm, player_name=self.name, role=role_str)

    def prompt_action(self, actions: List[str]) -> int:
        self.state.actions = actions
        self.adventure_agent.update_state(
            observations=self.history.get_history_str(),
            tasks=self.get_task_to_complete(),
            actions=actions,
            current_location=self.state.location.value,
        )
        prompts, chosen_action = self.adventure_agent.act()
        self.state.llm_responses = self.adventure_agent.responses
        self.state.response = str(chosen_action)
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
        self.voting_agent.update_state(
            observation=self.history.get_history_str(), actions=voting_actions
        )
        vote_prompt, vote = self.voting_agent.choose_action(self.get_message_str())
        self.state.llm_responses = self.voting_agent.responses
        self.state.response = str(vote)
        self.state.prompt = vote_prompt
        return vote

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
