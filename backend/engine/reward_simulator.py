"""Reward Simulation Engine.

Simulates annual reward earnings for different spending patterns.
Used for ranking optimization and personalized card recommendations.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class RewardSimulator:
    """Simulate reward earnings for credit cards."""
    
    def __init__(self, card_data: Dict):
        """Initialize simulator with card reward rates and fees."""
        self.card_name = card_data.get("card_name", "Unknown Card")
        self.annual_fee = card_data.get("annual_fee", 0.0)
        self.reward_rates = card_data.get("reward_rates", {})
        self.milestones = card_data.get("milestones", [])
        self.caps = card_data.get("caps", {})
    
    def calculate_annual_reward(
        self,
        spend_by_category: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Simulate annual reward earnings.
        
        Args:
            spend_by_category: {
                "online_shopping": float,
                "dining": float,
                "travel": float,
                "groceries": float,
                "fuel": float,
                "utilities": float,
                "general": float,
            }
        
        Returns:
            {
                "yearly_reward": float,
                "category_breakdown": Dict,
                "milestone_bonus": float,
                "total_annual_benefit": float,
                "net_benefit": float (after annual fee),
            }
        """
        category_breakdown = {}
        total_reward = 0.0
        total_spend = 0.0
        
        # Calculate rewards by category
        for category, spend in spend_by_category.items():
            rate = self.reward_rates.get(category, 0.0)
            category_reward = spend * rate
            
            # Apply caps if defined
            if category in self.caps:
                category_reward = min(category_reward, self.caps[category])
            
            category_breakdown[category] = {
                "spend": spend,
                "rate": rate,
                "reward": category_reward,
            }
            
            total_reward += category_reward
            total_spend += spend
        
        # Check milestones
        milestone_bonus = self._calculate_milestone_bonus(total_spend)
        
        # Net benefit
        total_annual_benefit = total_reward + milestone_bonus
        net_benefit = total_annual_benefit - self.annual_fee
        
        return {
            "card_name": self.card_name,
            "annual_fee": self.annual_fee,
            "total_spend": total_spend,
            "category_breakdown": category_breakdown,
            "total_reward_points": total_reward,
            "milestone_bonus": milestone_bonus,
            "total_annual_benefit": total_annual_benefit,
            "net_benefit": net_benefit,
            "roi_percent": (net_benefit / total_spend * 100) if total_spend > 0 else 0,
        }
    
    def _calculate_milestone_bonus(self, annual_spend: float) -> float:
        """Calculate milestone bonus based on annual spend."""
        bonus = 0.0
        
        for milestone in self.milestones:
            threshold = milestone.get("threshold", 0)
            milestone_bonus = milestone.get("bonus", 0)
            
            if annual_spend >= threshold:
                bonus = max(bonus, milestone_bonus)
        
        return bonus
    
    def rank_by_net_benefit(
        self,
        spend_pattern: Dict[str, float]
    ) -> float:
        """Calculate net benefit for ranking cards."""
        result = self.calculate_annual_reward(spend_pattern)
        return result.get("net_benefit", 0.0)


def simulate_for_persona(
    persona_spend: Dict[str, float],
    cards: List[Dict]
) -> List[Dict]:
    """
    Simulate rewards for a spending persona across multiple cards.
    
    Args:
        persona_spend: Spending pattern for persona
        cards: List of card data
    
    Returns:
        Ranked results
    """
    results = []
    
    for card_data in cards:
        simulator = RewardSimulator(card_data)
        simulation = simulator.calculate_annual_reward(persona_spend)
        results.append(simulation)
    
    # Sort by net benefit
    results.sort(key=lambda x: x.get("net_benefit", 0), reverse=True)
    
    return results


def generate_simulation_dataset(
    output_file: Optional[Path] = None
) -> Dict:
    """
    Generate reward simulations for all standard personas.
    
    Standard personas:
    - High earner (₹50L+ annual spend, 40% dining/travel)
    - Online shopper (₹25L annual spend, 50% online)
    - Family spender (₹30L annual spend, balanced)
    - Minimalist (₹10L annual spend, focused)
    - Traveler (₹35L annual spend, 45% travel)
    """
    personas = {
        "high_earner": {
            "annual_spend": 500000,
            "online_shopping": 0.20,
            "dining": 0.25,
            "travel": 0.25,
            "utilities": 0.10,
            "groceries": 0.10,
            "fuel": 0.05,
            "general": 0.05,
        },
        "online_shopper": {
            "annual_spend": 250000,
            "online_shopping": 0.50,
            "dining": 0.15,
            "travel": 0.10,
            "utilities": 0.10,
            "groceries": 0.10,
            "fuel": 0.03,
            "general": 0.02,
        },
        "family_spender": {
            "annual_spend": 300000,
            "online_shopping": 0.25,
            "dining": 0.20,
            "travel": 0.15,
            "utilities": 0.15,
            "groceries": 0.15,
            "fuel": 0.07,
            "general": 0.03,
        },
        "minimalist": {
            "annual_spend": 100000,
            "online_shopping": 0.20,
            "dining": 0.15,
            "travel": 0.10,
            "utilities": 0.25,
            "groceries": 0.20,
            "fuel": 0.05,
            "general": 0.05,
        },
        "traveler": {
            "annual_spend": 350000,
            "online_shopping": 0.15,
            "dining": 0.20,
            "travel": 0.45,
            "utilities": 0.05,
            "groceries": 0.08,
            "fuel": 0.04,
            "general": 0.03,
        },
    }
    
    # Load cards
    cards_file = DATA_DIR / "cards" / "cards_master_schema.json"
    if not cards_file.exists():
        return {
            "status": "error",
            "message": "No card data found",
        }
    
    with cards_file.open("r", encoding="utf-8") as f:
        cards = json.load(f)
    
    simulations = {}
    
    for persona_name, persona_spend_pct in personas.items():
        annual_spend = persona_spend_pct.pop("annual_spend")
        
        # Convert percentages to absolute spend
        spend_pattern = {
            cat: annual_spend * pct
            for cat, pct in persona_spend_pct.items()
        }
        
        persona_results = simulate_for_persona(spend_pattern, cards)
        simulations[persona_name] = {
            "annual_spend": annual_spend,
            "spend_pattern": spend_pattern,
            "top_3_cards": persona_results[:3],
            "all_cards": persona_results,
        }
    
    # Save simulations
    if output_file is None:
        output_file = DATA_DIR / "simulations" / "reward_simulation_dataset.json"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(simulations, f, indent=2)
    
    return {
        "status": "completed",
        "worker": "reward_simulator",
        "personas_simulated": len(personas),
        "cards_evaluated": len(cards),
        "output_file": str(output_file),
        "generated_at": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    # Test simulator
    sample_card = {
        "card_name": "Test Card",
        "annual_fee": 500,
        "reward_rates": {
            "online_shopping": 0.05,
            "dining": 0.03,
            "travel": 0.03,
            "utilities": 0.01,
            "groceries": 0.02,
            "fuel": 0.01,
            "general": 0.01,
        },
        "milestones": [
            {"threshold": 300000, "bonus": 2000},
            {"threshold": 500000, "bonus": 5000},
        ],
    }
    
    sample_spend = {
        "online_shopping": 50000,
        "dining": 40000,
        "travel": 60000,
        "utilities": 30000,
        "groceries": 30000,
        "fuel": 10000,
        "general": 5000,
    }
    
    simulator = RewardSimulator(sample_card)
    result = simulator.calculate_annual_reward(sample_spend)
    print(json.dumps(result, indent=2))
