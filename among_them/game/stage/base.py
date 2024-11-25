from typing import ClassVar, Self
from pydantic import BaseModel

from abc import ABC, abstractmethod


class Stage(BaseModel, ABC):
    _stages: ClassVar[dict[str, type[Self]]]
    TYPE: ClassVar[str]
    player_to_act: int

    def __init_subclass__(cls) -> None:
        cls._stages[cls.TYPE] = cls

    @classmethod
    def dispatch(cls, model: dict) -> Self:
        return cls._stages[model["TYPE"]].model_validate(model)

    def perform_step(self) -> bool:
        ...
