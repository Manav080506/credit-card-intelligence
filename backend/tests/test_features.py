from backend.engine.feature_engineering import build_features


def test_build_features_has_entropy_and_ratios():
    spend = {
        'online_shopping': 10000,
        'dining': 5000,
        'travel': 5000,
        'utilities': 5000,
    }
    features = build_features(spend)
    assert 'spend_entropy' in features
    assert 0 <= features['online_ratio'] <= 1
    assert 0 <= features['dining_ratio'] <= 1
    assert 0 <= features['travel_ratio'] <= 1
    assert 0 <= features['utility_ratio'] <= 1
