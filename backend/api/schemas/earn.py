from pydantic import BaseModel

class EarnRequest(BaseModel):
    card_id: str
    amount: float
    category: str

class EarnResponse(BaseModel):
    reward_amount: float
    reward_unit: str | None
    cap_applied: bool
    explanation: str
    metadata: dict
