from fastapi import APIRouter

from backend.workers.card_discovery_worker import discover_cards


router = APIRouter(

    prefix="/discover_cards",

    tags=["Discovery"]

)


@router.post("")

def discover():

    return discover_cards()
