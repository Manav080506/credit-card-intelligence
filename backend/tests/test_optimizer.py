from backend.engine.optimizer import optimize_spend


def test_optimize_spend_returns_best_card():
    payload = {
        'online_shopping': 15000,
        'dining': 3000,
        'travel': 2000,
        'utilities': 1000,
    }
    result = optimize_spend(payload)
    assert 'best_card' in result
    assert 'expected_monthly_reward' in result
    assert result['expected_monthly_reward'] >= 0
