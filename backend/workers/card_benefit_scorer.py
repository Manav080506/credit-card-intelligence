"""
Worker: Card Benefit Scorer

Goal:
Calculate usefulness score of a credit card.

Factors:
- higher reward_rate = better score
- more bonus categories = better
- higher annual fee = penalty
- cashback preferred over points

Score range: 0-100

Output:
{
 "card_id": str,
 "benefit_score": float,
 "breakdown":{
     "reward_score": float,
     "fee_penalty": float,
     "category_score": float
 }
}
"""

from typing import Any, Dict, List


class CardBenefitScorer:
    """Calculates overall card benefit score in the 0-100 range."""

    # Relative influence of each component in the final score.
    REWARD_WEIGHT = 0.60
    CATEGORY_WEIGHT = 0.25
    FEE_WEIGHT = 0.15

    # Practical caps to normalize raw card fields.
    MAX_EFFECTIVE_REWARD_RATE = 10.0
    MAX_EFFECTIVE_ANNUAL_FEE = 10000.0
    MAX_EFFECTIVE_BONUS_CATEGORIES = 8

    # Reward type preference boost/penalty.
    REWARD_TYPE_BONUS = {
        "cashback": 1.0,
        "cash_back": 1.0,
        "cash back": 1.0,
        "points": 0.6,
    }

    def score_card(self, card: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute card benefit score.

        Args:
            card: Card json following current card schema.

        Returns:
            {
              "card_id": str,
              "benefit_score": float,
              "breakdown": {
                  "reward_score": float,
                  "fee_penalty": float,
                  "category_score": float
              }
            }
        """
        card_id = card.get("card_id", "unknown")

        reward_score = self._reward_score(card)
        category_score = self._category_score(card)
        fee_penalty = self._fee_penalty(card)

        weighted_reward = reward_score * self.REWARD_WEIGHT
        weighted_category = category_score * self.CATEGORY_WEIGHT
        weighted_fee_penalty = fee_penalty * self.FEE_WEIGHT

        benefit_score = weighted_reward + weighted_category - weighted_fee_penalty
        benefit_score = self._clamp(benefit_score, 0.0, 100.0)

        return {
            "card_id": card_id,
            "benefit_score": round(benefit_score, 2),
            "breakdown": {
                "reward_score": round(reward_score, 2),
                "fee_penalty": round(fee_penalty, 2),
                "category_score": round(category_score, 2),
            },
        }

    def _reward_score(self, card: Dict[str, Any]) -> float:
        """Reward score driven by average reward rate and reward type preference."""
        earn_rules: List[Dict[str, Any]] = card.get("earn_rules", [])

        if not earn_rules:
            base_rate_score = 0.0
        else:
            rates = [
                float(rule.get("reward_rate", 0.0) or 0.0)
                for rule in earn_rules
            ]
            avg_rate = sum(rates) / len(rates)
            normalized_rate = avg_rate / self.MAX_EFFECTIVE_REWARD_RATE
            base_rate_score = self._clamp(normalized_rate, 0.0, 1.0) * 100.0

        reward_type = str(card.get("reward_type", "points")).strip().lower()
        type_multiplier = self.REWARD_TYPE_BONUS.get(reward_type, 0.6)

        reward_score = base_rate_score * type_multiplier
        return self._clamp(reward_score, 0.0, 100.0)

    def _category_score(self, card: Dict[str, Any]) -> float:
        """Category score based on number of bonus categories above baseline rewards."""
        earn_rules: List[Dict[str, Any]] = card.get("earn_rules", [])

        if not earn_rules:
            return 0.0

        rates = [float(rule.get("reward_rate", 0.0) or 0.0) for rule in earn_rules]
        baseline = min(rates) if rates else 0.0

        bonus_categories = [
            rule for rule in earn_rules
            if float(rule.get("reward_rate", 0.0) or 0.0) > baseline
        ]
        bonus_count = len(bonus_categories)

        normalized = bonus_count / float(self.MAX_EFFECTIVE_BONUS_CATEGORIES)
        return self._clamp(normalized, 0.0, 1.0) * 100.0

    def _fee_penalty(self, card: Dict[str, Any]) -> float:
        """Fee penalty scaled to 0-100 based on annual fee."""
        fees = card.get("fees", {})
        annual_fee = float(fees.get("annual_fee", 0.0) or 0.0)

        normalized = annual_fee / self.MAX_EFFECTIVE_ANNUAL_FEE
        return self._clamp(normalized, 0.0, 1.0) * 100.0

    @staticmethod
    def _clamp(value: float, low: float, high: float) -> float:
        return max(low, min(value, high))


def score_card_benefit(card: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to score a single card json."""
    scorer = CardBenefitScorer()
    return scorer.score_card(card)
