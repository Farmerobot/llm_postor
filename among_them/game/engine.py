from typing import ClassVar, overload

from pydantic import Field

from among_them.game.player.base import Player
from among_them.game.player.fake import FakeAI
from among_them.game.player.llm import LLM


class Engine:
    players: list[Player] | None = None
    reported: bool = False
    debug: bool = True
    stage: Stage
    state_path: str | None = None

    @overload
    def load_players(
        self, impostor_model: str, crewmate_model: str, n_impostors: int
    ) -> None:
        ...

    @overload
    def load_players(self, llms: list[LLM], impostors: list[int]) -> None:
        ...

    @overload
    def load_players(self, llms: list[LLM], n_impostors: int) -> None:
        ...

    @overload
    def load_players(self, players: list[Player]) -> None:
        ...

    @overload
    def load_players(self, players: list[Player], impostors: list[int]) -> None:
        ...

    @overload
    def load_players(self, players: list[Player], n_impostors: int) -> None:
        ...

    def loop(self) -> None:
        ...

    def perform_step(self) -> bool:
        ...

    def n_rounds(self) -> int:
        ...
