from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from backend.engine.gap_recommender import recommend_card_for_gaps


router = APIRouter(

    prefix="/recommend_next",

    tags=["Recommend"]

)


class GapRequest(BaseModel):

    current_cards: List[str]

    monthly_spend: Dict[str, float]


@router.post("")

def recommend_next(payload: GapRequest):

    return recommend_card_for_gaps(

        current_cards=payload.current_cards,

        monthly_spend=payload.monthly_spend

    )
