from langchain_openai import ChatOpenAI
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from typing import Any, List
from pydantic import BaseModel, Field
import datetime

class GameState(BaseModel):
    history: list[str] = Field(default_factory=list)

class DiscussionAgent(BaseModel):
    llm: Any
    state: GameState = Field(default_factory=GameState)
    player_name: str = ""
    role: str = ""

    class Config:
        arbitrary_types_allowed = True

    def update_state(self, observation: str):
        self.state.history.append(observation)

    def create_discussion_points(self) -> str:
        discussion_template = """
        You are {player_name}, a player in an Among Us-like game. You are participating in the discussion phase.
        You are {player_role}.

        Game history and your observations:
        {history}
        
        Based on the game history and your observations, create discussion points to share with other players.
        Be strategic about what information you reveal. If you're an impostor, you might want to lie or misdirect.
        If you're a crewmate, share your observations but be aware that others might be lying.
        
        Your discussion points:
        """
        
        discussion_prompt = discussion_template.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history)
        )
        
        discussion_points = self.llm.predict(discussion_prompt)
        save_path = f"src/game/game_results/discussion/discussion_points_{self.player_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(save_path, "w") as f:
            f.write(discussion_points.strip())
        return discussion_points.strip()

    def respond_to_statements(self, statements: str) -> str:
        response_template = """
        You are {player_name}, a player in an Among Us-like game. You are participating in the discussion phase.
        This is turn-based game where players take turns making actions and responding to each other.
        There are no actions like venting or sabotaging in this game.

        You are {player_role}.
        
        Game history and your observations:
        {history}
        
        Recent statements from other players:
        {statements}
        
        Respond to these statements based on the game history, your observations, and what you know about the game.
        Be strategic in your response. If you're an impostor, you might want to support or cast doubt on certain statements.
        If you're a crewmate, you might want to corroborate or question statements based on your observations.
        Respond should be short and to the point. You don't need to respond to every statement.
        You don't need write your name in brackets, it's already included in the prompt.

        Your response:
        """
        
        response_prompt = response_template.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history),
            statements=statements
        )
        
        response = self.llm.predict(response_prompt)
        # save_path = f"statements_{self.player_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        # with open(save_path, "w") as f:
        #     f.write(response.strip())
        return response.strip()

# Example usage:
# llm = ChatOpenAI(temperature=0.7)
# game_state = GameState()
# agent = DiscussionAgent(llm=llm, state=game_state, player_name="Red")
# agent.update_state("Red saw Blue in Electrical")
# discussion_points = agent.create_discussion_points()
# statements = [
#     "[Blue]: I was in Medbay the whole time",
#     "[Green]: I saw Yellow near the body",
#     "[Yellow]: I was doing tasks in Navigation"
# ]
# response = agent.respond_to_statements(statements)