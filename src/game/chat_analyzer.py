from typing import List, Dict
from pydantic import BaseModel
from game.players.base_player import Player
from langchain_openai import ChatOpenAI
from llm_prompts import PERSUASION_TECHNIQUES
import re

class ChatAnalyzer(BaseModel):
    players: List[Player]
    llm_model_name: str = "gpt-3.5-turbo"
    persuasive_tricks: str = PERSUASION_TECHNIQUES

    def analyze(self) -> Dict[str, Dict[str, int]]:
        llm = ChatOpenAI(model=self.llm_model_name, temperature=0.1)
        results = {}

        # Get messages from the first player
        messages = self.players[0].get_message_str()
        
        # Extract messages by player
        player_messages = self.extract_player_messages(messages)

        for player_name, player_msgs in player_messages.items():
            prompt = f"Analyze the following messages and count how many times each of the following persuasive tricks are used:\n{self.persuasive_tricks}\n\nMessages:\n{player_msgs}"
            response = llm(prompt)
            results[player_name] = self.parse_response(response)

        return results

    def extract_player_messages(self, messages: str) -> Dict[str, str]:
        player_messages = {}
        pattern = re.compile(r'\[([^\]]+)\]: (.+)')
        
        for line in messages.split('\n'):
            match = pattern.search(line)
            if match:
                player_name = match.group(1)
                message = match.group(2)
                if player_name not in player_messages:
                    player_messages[player_name] = ""
                player_messages[player_name] += message + "\n"
        
        return player_messages

    def parse_response(self, response: str) -> Dict[str, int]:
        tricks_count = {}
        lines = response.split("\n")
        for line in lines:
            if ":" in line:
                trick, count = line.split(":")
                tricks_count[trick.strip()] = int(count.strip())
        return tricks_count