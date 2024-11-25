from typing import Self, overload

from pydantic import BaseModel

from among_them import utils
from among_them.consts import COSTS_PATH


class Cost(BaseModel):
    input_tokens: float
    cache_read: float
    output_tokens: float

    def __add__(self, o: Self) -> Self:
        return self.__class__(
            input_tokens=self.input_tokens + o.input_tokens,
            cache_read=self.cache_read + o.cache_read,
            output_tokens=self.output_tokens + o.output_tokens,
        )

    @overload
    def __truediv__(self, o: Self) -> Self:
        return self.__class__(
            input_tokens=self.input_tokens / o.input_tokens,
            cache_read=self.cache_read / o.cache_read,
            output_tokens=self.output_tokens / o.output_tokens,
        )

    @overload
    def __truediv__(self, o: int) -> Self:
        return self.__class__(
            input_tokens=self.input_tokens / o,
            cache_read=self.cache_read / o,
            output_tokens=self.output_tokens / o,
        )


TOKEN_COSTS = {
    key: Cost.model_validate(value)
    for key, value in utils.read_toml(COSTS_PATH, quit=True).items()
}
