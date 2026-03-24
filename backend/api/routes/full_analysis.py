from fastapi import APIRouter
from typing import Dict

from backend.workers.orchestrator import run_full_analysis


router = APIRouter(

    prefix="/full_analysis",

    tags=["Full Analysis"]

)


@router.post("")
def full_analysis(

    payload: Dict

):

    return run_full_analysis(payload)
