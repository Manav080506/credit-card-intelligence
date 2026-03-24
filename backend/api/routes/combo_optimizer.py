from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.engine.combo_optimizer import find_best_2_card_combo


router = APIRouter(
    prefix="/optimize_combo",
    tags=["Optimizer"]
)


class ComboRequest(BaseModel):

    card_ids: List[str]

    monthly_spend: Dict[str, float]


@router.post("")
def optimize_combo(payload: ComboRequest):

    return find_best_2_card_combo(
        all_card_ids=payload.card_ids,
        monthly_spend=payload.monthly_spend
    )
