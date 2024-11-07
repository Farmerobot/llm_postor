from typing import List, Any

from pydantic import Field
from .base_agent import Agent
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from llm_postor.game.llm_prompts import DISCUSSION_TEMPLATE
from llm_postor.game.llm_prompts import DISCUSSION_RESPONSE_TEMPLATE
from llm_postor.config import OPENROUTER_API_KEY
from llm_postor.game.agents.usage_metadata import UsageMetadata

class DiscussionAgent(Agent):
    llm: ChatOpenAI = None
    llm_model_name: str
    history: str = Field(default="")
    messages: List[str] = Field(default_factory=list)

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
            temperature=0.5
        )

    def act(
        self,
        observations: str,
        messages: List[str],
    ) -> Any:
        self.history = observations
        self.messages = messages

        points_prompt, points = self.create_discussion_points()
        response_prompt, response = self.respond_to_statements(points=points)
        self.responses.append(points)
        self.responses.append(response)
        return (
            f"Points prompt: {points_prompt}\n\nResponse prompt: {response_prompt}",
            response,
        )

    def create_discussion_points(self) -> str:
        discussion_prompt = DISCUSSION_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            history=self.history,
            statements=self.messages,
        )
        # print("\nDiscussion prompt:", discussion_prompt)
        discussion_points = self.llm.invoke([HumanMessage(content=discussion_prompt)])
        # print("\nDiscussion points:", discussion_points)
        self.add_token_usage(discussion_points.usage_metadata)
        return discussion_prompt, discussion_points.content.strip()

    def respond_to_statements(self, points: str) -> str:
        response_prompt = DISCUSSION_RESPONSE_TEMPLATE.format(
            player_name=self.player_name,
            player_role=self.role,
            points=points,
            history="\n".join(self.history),
            statements=self.messages,
        )
        # print("\nResponse prompt:", response_prompt)
        response = self.llm.invoke([HumanMessage(content=response_prompt)])
        # print("\nResponse:", response.content)
        self.add_token_usage(response.usage_metadata)
        return response_prompt, response.content.strip()
