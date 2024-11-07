import random
from typing import List
from pydantic import Field

from llm_postor.game.players.base_player import Player, PlayerRole

class FakeAIPlayer(Player):
    llm_model_name: str
    
    def prompt_action(self, actions: List[str]) -> int:
        random_action = random.randint(0, len(actions) - 1)
        self.state.actions = actions
        self.state.prompts = "I am a fake AI, choosing the random action"
        self.state.response = str(random_action)
        self.state.llm_responses = ["This is a placeholder LLM response."]
        self.state.observations = ["This is a placeholder observation."]
        return random_action

    def prompt_discussion(self) -> str:
        self.state.prompts = "I am a fake AI, saying nothing interesting"
        self.state.response = "I am a fake AI"
        self.state.llm_responses = ["This is a placeholder LLM response."]
        self.state.observations = ["This is a placeholder observation."]
        return "I am a fake AI"

    def prompt_vote(self, voting_actions: List[str], dead_players: List[str]) -> int:
        random_player = random.randint(0, len(voting_actions) - 1)
        self.state.actions = voting_actions
        self.state.prompts = "I am a fake AI, voting for the first player"
        self.state.response = str(random_player)
        self.state.llm_responses = ["This is a placeholder LLM response."]
        self.state.observations = ["This is a placeholder observation."]
        return random_player

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
