from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


from backend.engine.statement_analyzer import analyze_statement


router = APIRouter(

    prefix="/analyze_statement",

    tags=["Statement Analyzer"]

)


class Transaction(BaseModel):

    merchant: str

    amount: float

    category: str


class StatementRequest(BaseModel):

    card_ids: List[str]

    transactions: List[Transaction]


@router.post("")
def analyze(payload: StatementRequest):

    return analyze_statement(

        card_ids=payload.card_ids,

        transactions=[
            t.dict()

            for t in payload.transactions
        ]

    )
