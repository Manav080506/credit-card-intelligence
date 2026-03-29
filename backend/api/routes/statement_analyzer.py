from fastapi import APIRouter

from pydantic import BaseModel

from typing import List, Optional

from backend.engine.statement_analyzer import analyze_statement


router = APIRouter(

    prefix="/analyze_statement",

    tags=["Statement Analyzer"]

)


class Transaction(BaseModel):

    merchant: str

    amount: float

    category: Optional[str] = None


class StatementRequest(BaseModel):

    card_ids: List[str]

    transactions: List[Transaction]


@router.post("")

def analyze(

    payload: StatementRequest

):

    return analyze_statement(

        card_ids=payload.card_ids,

        transactions=[

            txn.dict()

            for txn in payload.transactions

        ]

    )
