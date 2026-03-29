"""
Cards API Routes - Card discovery, retrieval, and filtering endpoints
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/cards", tags=["Cards"])


# Card data structure for responses
class CardResponse:
    def __init__(self, id: str, bank: str, segment: str, annual_fee: int, 
                 reward_currency: str, lounge_domestic: int, credit_score: int):
        self.id = id
        self.bank = bank
        self.segment = segment
        self.annual_fee = annual_fee
        self.reward_currency = reward_currency
        self.lounge_domestic = lounge_domestic
        self.credit_score = credit_score


@router.get("")
def list_all_cards(
    segment: Optional[str] = Query(None, description="Filter by segment (cashback, travel, etc)"),
    bank: Optional[str] = Query(None, description="Filter by bank"),
    annual_fee_min: Optional[int] = Query(None, description="Minimum annual fee"),
    annual_fee_max: Optional[int] = Query(None, description="Maximum annual fee"),
    limit: int = Query(50, description="Number of cards to return")
):
    """
    Get all cards with optional filtering.
    
    Filters:
    - segment: cashback, travel, beginner, co-branded, premium
    - bank: HDFC, ICICI, Axis, SBI, Amex
    - annual_fee_min/max: Filter by annual fee range
    - limit: Number of results
    """
    # Stub: Real implementation queries PostgreSQL cards table
    # SELECT * FROM cards WHERE ... LIMIT limit
    return {
        "count": 0,
        "cards": [],
        "filters": {
            "segment": segment,
            "bank": bank,
            "annual_fee_min": annual_fee_min,
            "annual_fee_max": annual_fee_max,
        }
    }


@router.get("/{card_id}")
def get_card_details(card_id: str):
    """
    Get detailed card information including reward rules and eligibility.
    
    Returns:
    - Card metadata
    - Reward rules per category
    - Eligibility criteria
    - Recent changes (audit trail)
    """
    # Stub: Real implementation queries PostgreSQL
    # SELECT c.*, r.* FROM cards c
    # LEFT JOIN reward_rules r ON c.id = r.card_id
    # WHERE c.id = card_id
    return {
        "card": {
            "id": card_id,
            "bank": "HDFC",
            "segment": "premium",
            "annual_fee": 2500,
            "reward_rules": [],
            "lounge_domestic": 2,
            "last_updated": datetime.utcnow().isoformat()
        }
    }


@router.get("/by-bank/{bank}")
def get_cards_by_bank(bank: str, limit: int = Query(50)):
    """
    Get all cards from a specific bank.
    
    Example: /cards/by-bank/HDFC
    """
    # Stub: Real implementation queries PostgreSQL
    # SELECT * FROM cards WHERE LOWER(bank) = LOWER(bank)
    return {
        "bank": bank,
        "count": 0,
        "cards": []
    }


@router.get("/segment/{segment}")
def get_cards_by_segment(segment: str, limit: int = Query(50)):
    """
    Get cards by segment category.
    
    Segments:
    - cashback: High cashback on everyday purchases
    - travel: Travel-focused rewards
    - beginner: For first-time credit card users
    - co-branded: Co-branded with airlines/hotels
    - premium: Premium tier with lounge access
    """
    # Stub: Real implementation
    # SELECT * FROM cards WHERE segment = segment LIMIT limit
    return {
        "segment": segment,
        "count": 0,
        "cards": []
    }


@router.get("/recommend-by-spend")
def recommend_cards_by_spend(
    online: float = Query(0, description="Monthly online shopping spend"),
    dining: float = Query(0, description="Monthly dining spend"),
    travel: float = Query(0, description="Monthly travel spend"),
    utilities: float = Query(0, description="Monthly utilities spend"),
    limit: int = Query(10, description="Number of recommendations")
):
    """
    Get card recommendations based on spending pattern.
    
    Analyzes spend across categories and returns best cards.
    Integrates with /v2/optimize endpoint for full optimization.
    """
    total_spend = online + dining + travel + utilities
    
    if total_spend == 0:
        raise HTTPException(status_code=400, detail="Spend categories cannot all be zero")
    
    # Stub: Real implementation uses recommend_with_explanation from engine
    return {
        "spend": {
            "online": online,
            "dining": dining,
            "travel": travel,
            "utilities": utilities,
            "total": total_spend
        },
        "recommendations": [],
        "confidence": 0.0
    }


@router.get("/search")
def search_cards(
    q: str = Query(..., description="Search query (card name, bank, feature)"),
    limit: int = Query(20)
):
    """
    Full-text search for cards.
    
    Searches across:
    - Card names
    - Bank names
    - Categories/tags
    - Features (lounge, forex, etc)
    """
    # Stub: Real implementation uses PostgreSQL full-text search
    # SELECT * FROM cards WHERE name ILIKE '%q%' OR bank ILIKE '%q%'
    return {
        "query": q,
        "count": 0,
        "results": []
    }


@router.get("/trending")
def get_trending_cards():
    """
    Get trending cards based on recommendation frequency.
    
    Returns cards most frequently recommended in past 30 days.
    """
    # Stub: Real implementation aggregates optimization_logs
    # SELECT recommended_card, COUNT(*) as recommendation_count
    # FROM optimization_logs
    # WHERE created_at > NOW() - INTERVAL '30 days'
    # GROUP BY recommended_card
    # ORDER BY recommendation_count DESC
    return {
        "trending": [],
        "period": "30_days"
    }


@router.get("/new")
def get_new_cards():
    """
    Get recently added or updated cards.
    
    Cards added in the past 7 days or recently modified.
    """
    # Stub: Real implementation
    # SELECT * FROM cards ORDER BY last_updated DESC LIMIT 50
    return {
        "new_cards": [],
        "period": "7_days"
    }


@router.get("/stats")
def get_cards_statistics():
    """
    Get dataset statistics.
    
    Returns:
    - Total card count
    - Count by bank
    - Count by segment
    - Average annual fee
    - Last update timestamp
    """
    # Stub: Real implementation aggregates cards table
    return {
        "total_cards": 0,
        "by_bank": {},
        "by_segment": {},
        "average_annual_fee": 0,
        "last_dataset_update": None
    }


@router.get("/health")
def cards_health():
    """
    Health check for cards system.
    
    Returns:
    - Database connection status
    - Card count
    - Last update time
    """
    # Stub: Real implementation checks database
    return {
        "status": "healthy",
        "card_count": 0,
        "database": "unknown",
        "last_update": None
    }
