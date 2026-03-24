from fastapi import APIRouter
from backend.engine.redeem_calculator import calculate_redemption
from backend.api.schemas.redeem import RedeemRequest, RedeemResponse

router = APIRouter(prefix="/redeem", tags=["Redeem"])

@router.post("", response_model=RedeemResponse)
def redeem_points(payload: RedeemRequest):
    return calculate_redemption(
        card_id=payload.card_id,
        points=payload.points
    )
