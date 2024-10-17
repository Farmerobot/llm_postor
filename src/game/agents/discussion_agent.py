from typing import List, Any
from .base_agent import Agent
from langchain.schema import HumanMessage
from llm_prompts import DISCUSSION_TEMPLATE, DISCUSSION_RESPONSE_TEMPLATE
import datetime

class DiscussionAgent(Agent):
    def update_state(self, observation: str, tasks: List[str] = None, actions: List[str] = None):
        self.state.history.append(observation)

    def create_discussion_points(self) -> str:
        discussion_prompt = DISCUSSION_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history),
        )
        discussion_points = self.llm.invoke([HumanMessage(content=discussion_prompt)])
        self.responses.append(f"Discussion points: {discussion_points.content.strip()}")
        return discussion_points.content.strip()

    def respond_to_statements(self, statements: str) -> str:
        response_prompt = DISCUSSION_RESPONSE_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history="\n".join(self.state.history),
            statements=statements,
        )
        response = self.llm.invoke([HumanMessage(content=response_prompt)])
        self.responses.append(response.content.strip())
        return response.content.strip()

    def act(self) -> Any:
        return self.create_discussion_points()
