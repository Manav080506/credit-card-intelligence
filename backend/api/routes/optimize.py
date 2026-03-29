import json
from pathlib import Path

from fastapi import APIRouter

from backend.engine.recommendation_engine import recommend_with_explanation
from backend.models.spend_model import SpendModel


DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'cards_optimizer_layer.json'

router = APIRouter(prefix='/v2', tags=['Optimization V2'])


@router.post('/optimize')
def optimize(payload: SpendModel):
    with DATA_FILE.open('r', encoding='utf-8') as file:
        cards = json.load(file)

    return recommend_with_explanation(payload.model_dump(), cards)
