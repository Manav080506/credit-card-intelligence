from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.engine.wallet_advisor import analyze_wallet


router = APIRouter(
    prefix="/analyze_wallet",
    tags=["Wallet Advisor"]
)


class WalletRequest(BaseModel):

    card_ids: List[str]

    monthly_spend: Dict[str, float]


@router.post("")
def wallet_advisor(
    payload: WalletRequest
):

    return analyze_wallet(

        payload.card_ids,

        payload.monthly_spend

    )
