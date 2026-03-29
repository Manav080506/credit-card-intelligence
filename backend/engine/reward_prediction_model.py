"""Real-time reward prediction model.

Ensemble regression model combining RandomForest and GradientBoosting.
Includes deterministic training and rule-based fallback when confidence is low.
"""

from __future__ import annotations

from typing import Dict, List, Any, Tuple
import importlib

HAS_SKLEARN = True
try:  # pragma: no cover
    np = importlib.import_module("numpy")
    sklearn_ensemble = importlib.import_module("sklearn.ensemble")
    sklearn_preprocessing = importlib.import_module("sklearn.preprocessing")
    GradientBoostingRegressor = sklearn_ensemble.GradientBoostingRegressor
    RandomForestRegressor = sklearn_ensemble.RandomForestRegressor
    StandardScaler = sklearn_preprocessing.StandardScaler
except Exception:  # pragma: no cover
    HAS_SKLEARN = False
    np = None
    GradientBoostingRegressor = None
    RandomForestRegressor = None
    StandardScaler = None


CATEGORIES = [
    "online_shopping",
    "dining",
    "travel",
    "groceries",
    "fuel",
    "utilities",
]

FEATURES = [
    "online_shopping_spend",
    "dining_spend",
    "travel_spend",
    "groceries_spend",
    "fuel_spend",
    "utilities_spend",
    "annual_fee",
    "reward_rate_online",
    "reward_rate_dining",
    "reward_rate_travel",
]


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_spend(spend: Dict[str, Any]) -> Dict[str, float]:
    spend = spend or {}
    normalized = {k: max(0.0, _to_float(spend.get(k, 0.0), 0.0)) for k in CATEGORIES}
    return normalized


def _card_features(spend: Dict[str, float], card: Dict[str, Any]) -> List[float]:
    reward_rates = card.get("reward_rates", {}) if isinstance(card.get("reward_rates"), dict) else {}
    return [
        spend["online_shopping"],
        spend["dining"],
        spend["travel"],
        spend["groceries"],
        spend["fuel"],
        spend["utilities"],
        _to_float(card.get("annual_fee", 0.0), 0.0),
        _to_float(reward_rates.get("online_shopping", 0.0), 0.0),
        _to_float(reward_rates.get("dining", 0.0), 0.0),
        _to_float(reward_rates.get("travel", 0.0), 0.0),
    ]


def _rule_based_reward(spend: Dict[str, float], card: Dict[str, Any]) -> float:
    reward_rates = card.get("reward_rates", {}) if isinstance(card.get("reward_rates"), dict) else {}
    yearly = 0.0
    for category in CATEGORIES:
        yearly += spend[category] * _to_float(reward_rates.get(category, reward_rates.get("general", 0.0)), 0.0) * 12.0
    yearly -= _to_float(card.get("annual_fee", 0.0), 0.0)
    return yearly


def _calc_confidence(rf_pred: float, gb_pred: float) -> float:
    spread = abs(rf_pred - gb_pred)
    magnitude = max(abs(rf_pred), abs(gb_pred), 1.0)
    normalized_spread = min(1.0, spread / magnitude)
    confidence = 1.0 - normalized_spread
    return round(max(0.0, min(1.0, confidence)), 3)


class RewardPredictionModel:
    """Ensemble regressor for card reward prediction."""

    def __init__(self) -> None:
        self.scaler = StandardScaler() if HAS_SKLEARN else None
        self.rf = RandomForestRegressor(
            n_estimators=250,
            max_depth=10,
            random_state=42,
            n_jobs=1,
        ) if HAS_SKLEARN else None
        self.gb = GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=3,
            random_state=42,
        ) if HAS_SKLEARN else None
        self.is_trained = False

    def train_model(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train ensemble on dataset records.

        Expected format per record:
        {
          "spend": {...},
          "card_id": "axis_ace",
          "yearly_reward": 13500,
          "card": {optional card details with annual_fee and reward_rates}
        }
        """
        if not HAS_SKLEARN:
            return {"status": "fallback", "trained": False, "reason": "sklearn unavailable"}

        rows: List[List[float]] = []
        targets: List[float] = []

        for row in dataset or []:
            spend = _normalize_spend(row.get("spend", {}))
            card = row.get("card", {}) if isinstance(row.get("card"), dict) else {}
            if not card:
                card = {
                    "annual_fee": _to_float(row.get("annual_fee", 0.0), 0.0),
                    "reward_rates": row.get("reward_rates", {}) if isinstance(row.get("reward_rates"), dict) else {},
                }

            feature_row = _card_features(spend, card)
            target = _to_float(row.get("yearly_reward", 0.0), 0.0)
            rows.append(feature_row)
            targets.append(target)

        if not rows:
            self.is_trained = False
            return {"status": "empty", "trained": False, "samples": 0}

        x = np.array(rows, dtype=float)
        y = np.array(targets, dtype=float)

        x_scaled = self.scaler.fit_transform(x)
        self.rf.fit(x_scaled, y)
        self.gb.fit(x_scaled, y)
        self.is_trained = True

        rf_pred = self.rf.predict(x_scaled)
        gb_pred = self.gb.predict(x_scaled)
        ensemble = (rf_pred + gb_pred) / 2.0
        mae = float(np.mean(np.abs(ensemble - y)))

        return {
            "status": "trained",
            "trained": True,
            "samples": len(rows),
            "features": FEATURES,
            "mae": round(mae, 4),
        }

    def predict_expected_reward(self, spend: Dict[str, Any], card: Dict[str, Any]) -> Dict[str, float]:
        """Predict yearly reward for a card, with confidence and fallback."""
        normalized_spend = _normalize_spend(spend)

        if not self.is_trained or not HAS_SKLEARN:
            fallback_reward = _rule_based_reward(normalized_spend, card)
            return {
                "predicted_reward": round(fallback_reward, 2),
                "confidence": 0.6,
                "used_fallback": True,
            }

        features = np.array([_card_features(normalized_spend, card)], dtype=float)
        features_scaled = self.scaler.transform(features)

        rf_pred = float(self.rf.predict(features_scaled)[0])
        gb_pred = float(self.gb.predict(features_scaled)[0])
        ensemble_pred = (rf_pred + gb_pred) / 2.0
        confidence = _calc_confidence(rf_pred, gb_pred)

        if confidence < 0.65:
            fallback_reward = _rule_based_reward(normalized_spend, card)
            return {
                "predicted_reward": round(fallback_reward, 2),
                "confidence": confidence,
                "used_fallback": True,
            }

        return {
            "predicted_reward": round(ensemble_pred, 2),
            "confidence": confidence,
            "used_fallback": False,
        }

    def predict_best_card(self, spend: Dict[str, Any], card_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict best card and expected reward for given spend profile."""
        if not card_dataset:
            return {"best_card": None, "predicted_reward": 0.0, "confidence": 0.0}

        scored: List[Dict[str, Any]] = []
        for card in card_dataset:
            pred = self.predict_expected_reward(spend, card)
            scored.append(
                {
                    "card": card,
                    "predicted_reward": pred["predicted_reward"],
                    "confidence": pred["confidence"],
                    "used_fallback": pred["used_fallback"],
                }
            )

        scored.sort(key=lambda x: x["predicted_reward"], reverse=True)
        top = scored[0]

        best_card = {
            "card_id": top["card"].get("card_id") or top["card"].get("id"),
            "card_name": top["card"].get("card_name") or top["card"].get("name"),
        }
        return {
            "best_card": best_card,
            "predicted_reward": round(top["predicted_reward"], 2),
            "confidence": round(top["confidence"], 3),
        }
