from typing import List

from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import Field

from among_them.config import OPENROUTER_API_KEY
from among_them.game.llm_prompts import VOTING_SYSTEM_PROMPT, VOTING_USER_PROMPT
from among_them.game.utils import check_action_valid

from .base_agent import Agent


class VotingAgent(Agent):
    llm: ChatOpenAI = None
    llm_model_name: str
    history: str = Field(default="")
    available_actions: List[str] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.init_llm()

    def init_llm(self):
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "Missing OpenRouter API key. "
                "Please set OPENROUTER_API_KEY in your environment."
            )
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=self.llm_model_name,
            temperature=0,
        )

    def act(
        self,
        observations: str,
        actions: List[str],
        discussion_log: str,
        dead_players: List[str],
    ) -> int:
        self.history = observations
        self.available_actions = actions

        system_prompt = VOTING_SYSTEM_PROMPT

        user_prompt = VOTING_USER_PROMPT.format(
            player_name=self.player_name,
            player_role=self.role,
            discussion_log=discussion_log,
            history=self.history,
            actions="\n".join(f"- {action}" for action in self.available_actions),
            dead_players=", ".join(dead_players),
        )

        # print("\nAction prompt voting:", user_prompt)
        chosen_action = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ])
        # print("\nVoted for:", chosen_action.content)
        self.add_token_usage(chosen_action.usage_metadata)
        chosen_action_str = chosen_action.content.strip()
        self.responses.append(chosen_action_str)
        vote_idx, _ = check_action_valid(
            self.available_actions, chosen_action_str, self.player_name
        )
        return [user_prompt], vote_idx
