from typing import List, Any
from .base_agent import Agent
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from llm_postor.game.llm_prompts import DISCUSSION_TEMPLATE
from llm_postor.game.llm_prompts import DISCUSSION_RESPONSE_TEMPLATE
from llm_postor.config import OPENROUTER_API_KEY

class DiscussionAgent(Agent):
    llm: ChatOpenAI = None
    llm_model_name: str

    def __init__(self, **data):
        super().__init__(**data)
        self.init_llm()

    def init_llm(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("Missing OpenRouter API key. Please set OPENROUTER_API_KEY in your environment.")
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=self.llm_model_name,
            temperature=0.1
        )

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
        # print("\nDiscussion prompt:", discussion_prompt)
        discussion_points = self.llm.invoke([HumanMessage(content=discussion_prompt)])
        # print("\nDiscussion points:", discussion_points)
        self.add_token_usage(discussion_points.usage_metadata)
        return discussion_prompt, discussion_points.content.strip()

    def respond_to_statements(self, statements: str, points: str) -> str:
        response_prompt = DISCUSSION_RESPONSE_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            points=points,
            history="\n".join(self.state.history),
            statements=statements,
        )
        # print("\nResponse prompt:", response_prompt)
        response = self.llm.invoke([HumanMessage(content=response_prompt)])
        # print("\nResponse:", response.content)
        self.add_token_usage(response.usage_metadata)
        return response_prompt, response.content.strip()

    def act(self) -> Any:
        points_prompt, points = self.create_discussion_points()
        response_prompt, response = self.respond_to_statements(
            statements=self.state.messages, points=points
        )
        self.responses.append(points)
        self.responses.append(response)
        return (
            f"Points prompt: {points_prompt}\n\nResponse prompt: {response_prompt}",
            response,
        )
