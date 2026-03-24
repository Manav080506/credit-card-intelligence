from fastapi import APIRouter
from backend.engine.card_comparator import compare_cards
from pydantic import BaseModel


router = APIRouter(prefix="/compare", tags=["Compare"])


class CompareRequest(BaseModel):
    cards: list[str]
    monthly_spend: dict


@router.post("")
def compare(payload: CompareRequest):
    return compare_cards(
        cards=payload.cards,
        monthly_spend=payload.monthly_spend
    )
