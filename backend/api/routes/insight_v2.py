from typing import Dict, List

from fastapi import APIRouter

from backend.engine.insight_engine_v2 import get_best_card_for_transactions
from backend.engine.optimizer import compare_cards, generate_ai_insight
from backend.engine.optimizer import optimize_spend as optimize_spend_with_dataset
from backend.workers.orchestrator import InsightOrchestratorV2


router = APIRouter(tags=["Insight V2"])


@router.post("/predict-card")
def predict_card(payload: Dict):
    transactions = payload.get("transactions", [])
    return get_best_card_for_transactions(transactions)


@router.post("/optimize-spend")
def optimize_spend(payload: Dict):
    return optimize_spend_with_dataset(payload)


@router.post("/compare-cards")
def compare_spend_cards(payload: Dict):
    return {"results": compare_cards(payload)}


@router.post("/ai-insights")
def ai_insights(payload: Dict):
    return {"insights": generate_ai_insight(payload)}


@router.post("/analyze-spend")
def analyze_spend(payload: Dict):
    transactions: List[Dict] = payload.get("transactions", [])
    orchestrator = InsightOrchestratorV2()
    return orchestrator.run_user_pipeline(transactions)


@router.get("/best-card")
def best_card():
    return get_best_card_for_transactions([])


@router.get("/reward-confidence")
def reward_confidence():
    result = get_best_card_for_transactions([])
    return {
        "best_card": result.get("best_card"),
        "confidence": result.get("confidence", 0),
    }
