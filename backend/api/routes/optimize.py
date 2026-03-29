from fastapi import APIRouter

from backend.engine.optimizer import optimize_spend
from backend.models.spend_model import SpendModel

router = APIRouter(tags=['Optimization V2'])


@router.post('/optimize')
def optimize(payload: SpendModel):
    return optimize_spend(payload.model_dump())


@router.post('/v2/optimize', include_in_schema=False)
def optimize_v2(payload: SpendModel):
    return optimize_spend(payload.model_dump())
