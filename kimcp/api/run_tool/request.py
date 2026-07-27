from typing import Any

from pydantic import BaseModel, Field


class RunToolRequest(BaseModel):
    args: dict[str, Any] = Field(default_factory=dict)
