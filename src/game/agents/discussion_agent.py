from typing import List, Any
from .base_agent import Agent
from langchain.schema import HumanMessage
from game.llm_prompts import DISCUSSION_TEMPLATE, DISCUSSION_RESPONSE_TEMPLATE


class DiscussionAgent(Agent):
    def update_state(
        self,
        observations: str,
        tasks: List[str] = None,
        actions: List[str] = None,
        messages: List[str] = None,
    ):
        self.state.history = observations
        self.state.messages = messages

    def create_discussion_points(self) -> str:
        discussion_prompt = DISCUSSION_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history=self.state.history,
            statements=self.state.messages,
        )
        discussion_points = self.llm.invoke([HumanMessage(content=discussion_prompt)])
        self.add_token_usage(discussion_points.usage_metadata)
        self.responses.append(f"Discussion points: {discussion_points.content.strip()}")
        return discussion_prompt, discussion_points.content.strip()

    def respond_to_statements(self, statements: str, points: str) -> str:
        response_prompt = DISCUSSION_RESPONSE_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            points=points,
            history="\n".join(self.state.history),
            statements=statements,
        )
        response = self.llm.invoke([HumanMessage(content=response_prompt)])
        self.add_token_usage(response.usage_metadata)
        self.responses.append(response.content.strip())
        return response_prompt, response.content.strip()

    def act(self) -> Any:
        points_prompt, points = self.create_discussion_points()
        response_prompt, response = self.respond_to_statements(
            statements=self.state.messages, points=points
        )
        return (
            f"Points prompt: {points_prompt}\n\nResponse prompt: {response_prompt}",
            response,
        )
