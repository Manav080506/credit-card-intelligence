from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.engine.compare_optimizer import compare_cards


router = APIRouter(
    prefix="/compare",
    tags=["Compare"]
)


class CompareRequest(BaseModel):

    card_ids: List[str] = []

    monthly_spend: Dict[str, float]


@router.post("")
def compare(payload: CompareRequest):

    return compare_cards(
        card_ids=payload.card_ids,
        sample_spend=payload.monthly_spend
    )
