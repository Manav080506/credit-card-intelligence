from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from backend.engine.combo_optimizer_v2 import find_best_combo


router = APIRouter(
    prefix="/best_combo",
    tags=["Combo Optimizer"]
)


class ComboRequest(BaseModel):

    monthly_spend: Dict[str, float]

    max_cards: int = 3


@router.post("")
def optimize_combo(payload: ComboRequest):

    return find_best_combo(

        monthly_spend=payload.monthly_spend,

        max_cards=payload.max_cards

    )
