from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List


from backend.engine.spend_simulator import simulate_spend_change


router = APIRouter(

    prefix="/simulate_spend",

    tags=["Spend Simulator"]

)


class SimulationRequest(BaseModel):

    card_ids: List[str]

    current_spend: Dict[str, float]

    new_spend: Dict[str, float]


@router.post("")
def simulate(payload: SimulationRequest):

    return simulate_spend_change(

        payload.card_ids,

        payload.current_spend,

        payload.new_spend

    )
