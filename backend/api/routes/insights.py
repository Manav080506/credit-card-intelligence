import json
from pathlib import Path

from fastapi import APIRouter

from backend.engine.explanation_engine import explain_recommendation
from backend.engine.feature_engineering import build_features
from backend.models.spend_model import SpendModel


DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'cards_optimizer_layer.json'

router = APIRouter(prefix='/v2', tags=['Insights V2'])


@router.post('/insights')
def insights(payload: SpendModel):
    with DATA_FILE.open('r', encoding='utf-8') as file:
        cards = json.load(file)

    features = build_features(payload.model_dump())
    sample_card = cards[0] if cards else {}
    explanation = explain_recommendation(sample_card, features)

    return {
        'features': features,
        'insight_summary': explanation.get('insight_summary', ''),
        'reason_codes': explanation.get('reason_codes', []),
        'reasons': explanation.get('reasons', []),
    }
