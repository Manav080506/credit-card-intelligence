from backend.engine.optimizer import optimize_spend


def test_optimize_spend_returns_best_card():
    payload = {
        'online_shopping': 15000,
        'dining': 3000,
        'travel': 2000,
        'groceries': 1000,
        'fuel': 500,
        'utilities': 1000,
    }
    result = optimize_spend(payload)
    assert 'top_cards' in result
    assert 'optimizer_confidence' in result
    assert len(result['top_cards']) >= 1
    assert result['top_cards'][0]['monthly_reward'] >= 0
