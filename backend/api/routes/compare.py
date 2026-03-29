from fastapi import APIRouter
import json
from pathlib import Path

from backend.engine.card_comparator import compare_cards
from backend.engine.recommendation_engine import rank_cards
from backend.models.spend_model import SpendModel
from pydantic import BaseModel


router = APIRouter(prefix="/compare", tags=["Compare"])

DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'cards_optimizer_layer.json'


class CompareRequest(BaseModel):
    cards: list[str]
    monthly_spend: dict


@router.post("")
def compare(payload: CompareRequest):
    return compare_cards(
        cards=payload.cards,
        monthly_spend=payload.monthly_spend
    )


@router.post("/v2")
def compare_v2(payload: SpendModel):
    with DATA_FILE.open('r', encoding='utf-8') as file:
        cards = json.load(file)
    return {"results": rank_cards(payload.model_dump(), cards)}
