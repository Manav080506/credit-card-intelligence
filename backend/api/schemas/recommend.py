from pydantic import BaseModel

class RecommendRequest(BaseModel):
    online_shopping: float
    food_dining: float
    travel: float
    utilities: float

class CardRecommendation(BaseModel):
    card_id: str
    card_name: str
    net_monthly_gain: float
    reasons: list[str]

class RecommendResponse(BaseModel):
    best_card: CardRecommendation
    alternatives: list[CardRecommendation]
