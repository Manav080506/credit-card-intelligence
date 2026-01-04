from pydantic import BaseModel

class RedeemRequest(BaseModel):
    card_id: str
    points: int

class RedeemOption(BaseModel):
    id: str
    type: str
    partner: str
    value: float
    value_per_point: float | None = None
    notes: str | None = None

class RedeemResponse(BaseModel):
    best_option: RedeemOption
    all_options: list[RedeemOption]
