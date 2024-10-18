from typing import List, Dict, Any
from pydantic import BaseModel

class RoundData(BaseModel):
    location: str
    observations: Dict[str, str]
    llm_responses: List[str]
    actions: List[str]
    
class PlayerHistory:
    def __init__(self):
        self.rounds: List[RoundData] = []

    def add_round(self, round_data: RoundData):
        self.rounds.append(round_data)

    def get_history(self) -> List[RoundData]:
        return self.rounds
    
    def get_history_str(self) -> str:
        history_str = ""
        for round in self.get_history():
            history_str += f"Location: {round.location}\n"
            history_str += f"Observations: {', '.join(round.observations)}\n"
            history_str += f"LLM Responses: {', '.join(round.llm_responses)}\n"
            history_str += f"Actions: {', '.join(round.actions)}\n\n"
        return history_str
