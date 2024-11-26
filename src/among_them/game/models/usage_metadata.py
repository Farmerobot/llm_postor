from openai import BaseModel
from pydantic import Field


class UsageMetadata(BaseModel):
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    cache_read: int = Field(default=0)
    cost: float = Field(default=0.0)

    def to_dict(self):
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cache_read": self.cache_read,
            "cost": self.cost,
        }
