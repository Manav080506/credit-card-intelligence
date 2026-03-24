from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.engine.wallet_optimizer import optimize_wallet


router = APIRouter(
    prefix="/optimize_wallet",
    tags=["Optimizer"]
)


class OptimizeWalletRequest(BaseModel):

    card_ids: List[str]

    monthly_spend: Dict[str, float]


@router.post("")
def optimize(payload: OptimizeWalletRequest):

    return optimize_wallet(
        card_ids=payload.card_ids,
        monthly_spend=payload.monthly_spend
    )
