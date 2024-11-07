import re
from typing import List, Dict
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from llm_postor.game.players.base_player import Player
from llm_postor.game.llm_prompts import ANNOTATION_SYSTEM_PROMPT

class ChatAnalyzer(BaseModel):
    players: List[Player]
    llm_model_name: str = "gpt-4o-mini"

    def analyze(self) -> Dict[str, Dict[str, int]]:
        llm = ChatOpenAI(model=self.llm_model_name, temperature=0)
        results = {}

        # Get messages from the first player
        messages = "\n".join(self.players[0].get_chat_messages())
        
        # Extract messages by player
        player_messages = self.extract_player_messages(messages)

        for player_name, player_msgs in player_messages.items():
            prompt = ANNOTATION_SYSTEM_PROMPT
            response = llm.invoke([
                SystemMessage(content=prompt),
                HumanMessage(content=player_msgs)
            ])
            results[player_name] = self.parse_response(response.content.strip())

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
        print(response)
        tricks_count = {}
        lines = response.split("\n")
        for line in lines:
            if ":" in line:
                trick, count = line.split(":")
                tricks_count[trick.strip()] = int(count.strip())
        return tricks_count