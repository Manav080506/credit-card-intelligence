from fastapi import APIRouter
from backend.engine.card_registry import list_cards

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("")
def get_cards():
    cards = list_cards()
    return {
        "count": len(cards),
        "cards": cards
    }

from backend.engine.card_registry import registry_health

@router.get("/health")
def cards_health():
    return registry_health()
