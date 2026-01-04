from fastapi import FastAPI

app = FastAPI(
    title="Credit Card Intelligence API",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

from backend.engine.earn_calculator import calculate_reward
from backend.api.schemas.earn import EarnRequest, EarnResponse

@app.post("/earn", response_model=EarnResponse)
def earn_rewards(payload: EarnRequest):
    return calculate_reward(
        card_id=payload.card_id,
        amount=payload.amount,
        category=payload.category
    )

from backend.engine.redeem_calculator import calculate_redemption
from backend.api.schemas.redeem import RedeemRequest, RedeemResponse

@app.post("/redeem", response_model=RedeemResponse)
def redeem_points(payload: RedeemRequest):
    return calculate_redemption(
        card_id=payload.card_id,
        points=payload.points
    )
