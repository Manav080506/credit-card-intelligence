from fastapi import APIRouter
from backend.engine.reward_stacker import calculate_stacked_rewards
from backend.api.schemas.earn import EarnRequest, EarnResponse

router = APIRouter(prefix="/earn", tags=["Earn"])

@router.post("")
def earn_rewards(payload: EarnRequest):
    return calculate_stacked_rewards(
        card_id=payload.card_id,
        amount=payload.amount,
        category=payload.category,
        platform_id=payload.platform_id
    )
