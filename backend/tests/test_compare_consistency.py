from backend.engine.card_comparison_evaluator import compare_cards
from backend.engine.response_formatter import format_top_cards
from backend.workers.manual_seed_loader import load_seed_cards


def _sample_spend():
    return {
        "online_shopping": 10000,
        "dining": 5000,
        "travel": 2000,
        "groceries": 3000,
        "fuel": 1000,
        "utilities": 4000,
    }


def test_top_card_order():
    cards = [
        {
            "card_id": "card_a",
            "card_name": "Card A",
            "annual_fee": 0,
            "reward_rates": {
                "online_shopping": 0.05,
                "dining": 0.02,
                "travel": 0.01,
                "groceries": 0.01,
                "fuel": 0.0,
                "utilities": 0.01,
                "general": 0.01,
            },
            "benefits": {"lounge_access": 2, "fuel_surcharge_waiver": True, "forex_markup": 3.5},
            "milestone_bonus": [],
            "confidence": 0.9,
        },
        {
            "card_id": "card_b",
            "card_name": "Card B",
            "annual_fee": 0,
            "reward_rates": {
                "online_shopping": 0.01,
                "dining": 0.01,
                "travel": 0.01,
                "groceries": 0.01,
                "fuel": 0.0,
                "utilities": 0.01,
                "general": 0.01,
            },
            "benefits": {"lounge_access": 0, "fuel_surcharge_waiver": False, "forex_markup": 3.5},
            "milestone_bonus": [],
            "confidence": 0.8,
        },
    ]

    result = compare_cards(cards, _sample_spend(), limit=2)
    assert result[0]["yearly_reward"] >= result[1]["yearly_reward"]


def test_compare_response_has_canonical_fields():
    cards = compare_cards(load_seed_cards(), _sample_spend())
    formatted = format_top_cards(cards)

    assert "top_cards" in formatted
    assert "optimizer_confidence" in formatted
    assert len(formatted["top_cards"]) > 0

    card = formatted["top_cards"][0]
    assert "card_id" in card
    assert "card_name" in card
    assert "monthly_reward" in card
    assert "yearly_reward" in card
    assert "confidence" in card
    assert "reason" in card
    assert "benefit_score" in card
    assert "reward_breakdown" in card


def test_spend_schema_supports_six_categories():
    cards = compare_cards(load_seed_cards(), _sample_spend())
    assert len(cards) > 0


def test_confidence_is_bounded_between_zero_and_one():
    cards = compare_cards(load_seed_cards(), _sample_spend())
    formatted = format_top_cards(cards)
    assert 0 <= formatted["optimizer_confidence"] <= 1


def test_reward_breakdown_has_numeric_values():
    cards = compare_cards(load_seed_cards(), _sample_spend())
    formatted = format_top_cards(cards)
    breakdown = formatted["top_cards"][0]["reward_breakdown"]
    for _, value in breakdown.items():
        assert isinstance(value, (int, float))
