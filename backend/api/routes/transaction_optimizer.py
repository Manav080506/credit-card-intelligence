from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.engine.transaction_optimizer import best_card_for_transaction


router = APIRouter(
    prefix="/best_card_for_txn",
    tags=["Transaction Optimizer"]
)


class TxnRequest(BaseModel):

    card_ids: List[str]

    amount: float

    category: str


@router.post("")
def optimize_txn(payload: TxnRequest):

    return best_card_for_transaction(

        card_ids=payload.card_ids,

        amount=payload.amount,

        category=payload.category

    )
