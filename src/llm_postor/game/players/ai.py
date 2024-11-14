from os import getenv
from typing import List
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from llm_postor.game.agents.adventure_agent import AdventureAgent
from llm_postor.game.agents.discussion_agent import DiscussionAgent
from llm_postor.game.agents.voting_agent import VotingAgent
from llm_postor.game.consts import TOKEN_COSTS
from llm_postor.game.players.base_player import Player, PlayerRole
from llm_postor.game.models.usage_metadata import UsageMetadata
from llm_postor.config import OPENROUTER_API_KEY

class AIPlayer(Player):
    llm_model_name: str

    def __init__(self, **data):
        super().__init__(**data)  # Initialize Player fields first
        self.adventure_agent = AdventureAgent(
            llm_model_name=self.llm_model_name, player_name=self.name, role=self.role.value
        )
        self.discussion_agent = DiscussionAgent(
            llm_model_name=self.llm_model_name, player_name=self.name, role=self.role.value
        )
        self.voting_agent = VotingAgent(
            llm_model_name=self.llm_model_name, player_name=self.name, role=self.role.value
        )

    def prompt_action(self, actions: List[str]) -> int:
        self.state.actions = actions
        prompts, chosen_action = self.adventure_agent.act(
            observations=self.history.get_history_str(),
            tasks=self.get_task_to_complete(),
            actions=actions,
            current_location=self.state.location.value,
            in_room=self.state.player_in_room,
        )
        self.state.llm_responses = self.adventure_agent.responses
        self.add_token_usage(self.adventure_agent.token_usage)
        self.state.response = str(chosen_action)
        self.state.prompts = prompts
        return chosen_action

    def prompt_discussion(self) -> str:
        history = self.history.get_history_str()
        statements = "\n".join(self.get_chat_messages())
        message_prompt, message = self.discussion_agent.act(
            observations=history, messages=statements
        )
        self.state.llm_responses = self.discussion_agent.responses
        self.add_token_usage(self.discussion_agent.token_usage)
        self.state.response = message
        self.state.prompts = message_prompt
        return message

    def prompt_vote(self, voting_actions: List[str], dead_players: List[str]) -> int:
        self.state.actions = voting_actions
        vote_prompt, vote = self.voting_agent.act(
            observations=self.history.get_history_str(),
            actions=voting_actions,
            discussion_log="\n".join(self.get_chat_messages()),
            dead_players=dead_players,
        )
        self.state.llm_responses = self.voting_agent.responses
        self.add_token_usage(self.voting_agent.token_usage)
        self.state.response = str(vote)
        self.state.prompts = vote_prompt
        return vote
    
    def add_token_usage(self, usage: UsageMetadata):
        self.state.token_usage.input_tokens += usage.input_tokens
        self.state.token_usage.output_tokens += usage.output_tokens
        self.state.token_usage.total_tokens += usage.total_tokens
        self.state.token_usage.cache_read += usage.cache_read
        
        for_model = self.llm_model_name
        previous_cost = self.state.token_usage.cost
        self.state.token_usage.cost = 0
        
        # if ends with :free, cost is 0
        if for_model.endswith(":free"):
            return
        if for_model not in TOKEN_COSTS:
            print(f"Model {for_model} not found in TOKEN_COSTS. defaulting to openai/gpt-4o-mini")
            for_model = "openai/gpt-4o-mini"
        million = 1_000_000
        self.state.token_usage.cost += self.state.token_usage.input_tokens * TOKEN_COSTS[for_model]["input_tokens"]/million
        self.state.token_usage.cost += self.state.token_usage.output_tokens * TOKEN_COSTS[for_model]["output_tokens"]/million
        self.state.token_usage.cost += self.state.token_usage.cache_read * TOKEN_COSTS[for_model]["cache_read"]/million
        print(f"\033[90m Player cost (action/total): {round(self.state.token_usage.cost-previous_cost, 6)}/{round(self.state.token_usage.cost, 6)} \033[00m")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
