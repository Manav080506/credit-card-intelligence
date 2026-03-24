from pydantic import BaseModel
from typing import Optional


class EarnRequest(BaseModel):
    card_id: str
    amount: float
    category: str
    platform_id: Optional[str] = None


class EarnResponse(BaseModel):
    card_reward: dict
    platform_reward: dict | None
    warnings: list[str]
