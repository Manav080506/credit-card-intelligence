from fastapi import APIRouter
from backend.engine.card_recommender import recommend_cards
from backend.api.schemas.recommend import RecommendRequest, RecommendResponse

router = APIRouter(prefix="/recommend", tags=["Recommend"])

@router.post("", response_model=RecommendResponse)
def recommend_card(payload: RecommendRequest):
    monthly_spend = payload.model_dump()
    return recommend_cards(monthly_spend=monthly_spend)
