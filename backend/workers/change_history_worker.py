"""
Worker: Change History Tracker

Goal:
Track how credit card benefits change over time.

Input:
- old card json
- new card json

Detects changes in:
- reward_rate
- annual_fee
- joining_fee
- reward_type
- monthly caps
- excluded categories

Output format:
{
 "card_id": str,
 "timestamp": str,
 "changes": [
  {
   "field": str,
   "old_value": any,
   "new_value": any
  }
 ]
}

Rules:
- if no change → return empty list
- store history inside: backend/data/history/{card_id}.json
- Append new change entries
- Do NOT overwrite old history
- Must work with current card schema.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

# Fields to monitor for changes
MONITORED_TOP_LEVEL = {"reward_type"}
MONITORED_FEES_FIELDS = {"annual_fee", "joining_fee"}
MONITORED_CONSTRAINT_FIELDS = {"monthly_caps", "excluded_categories"}


class ChangeHistoryWorker:
    """Tracks changes in credit card benefits over time."""
    
    def __init__(self, history_dir: str = "backend/data/history"):
        """
        Initialize the worker.
        
        Args:
            history_dir: Directory where history files will be stored
        """
        self.history_dir = history_dir
        os.makedirs(history_dir, exist_ok=True)
    
    def detect_changes(
        self, old_card: Dict[str, Any], new_card: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect changes between old and new card configurations.
        
        Args:
            old_card: Old card JSON
            new_card: New card JSON
            
        Returns:
            List of change dictionaries with field, old_value, new_value
        """
        changes = []
        
        # Check top-level fields (reward_type)
        for field in MONITORED_TOP_LEVEL:
            if field in old_card and field in new_card:
                old_val = old_card[field]
                new_val = new_card[field]
                if old_val != new_val:
                    changes.append({
                        "field": field,
                        "old_value": old_val,
                        "new_value": new_val
                    })
        
        # Check fees
        old_fees = old_card.get("fees", {})
        new_fees = new_card.get("fees", {})
        for field in MONITORED_FEES_FIELDS:
            old_val = old_fees.get(field)
            new_val = new_fees.get(field)
            if old_val != new_val:
                changes.append({
                    "field": f"fees.{field}",
                    "old_value": old_val,
                    "new_value": new_val
                })
        
        # Check constraints (monthly_caps, excluded_categories)
        old_constraints = old_card.get("constraints", {})
        new_constraints = new_card.get("constraints", {})
        for field in MONITORED_CONSTRAINT_FIELDS:
            old_val = old_constraints.get(field)
            new_val = new_constraints.get(field)
            if old_val != new_val:
                changes.append({
                    "field": f"constraints.{field}",
                    "old_value": old_val,
                    "new_value": new_val
                })
        
        # Check earn_rules for reward_rate changes
        changes.extend(self._detect_earn_rules_changes(
            old_card.get("earn_rules", []),
            new_card.get("earn_rules", [])
        ))
        
        return changes
    
    def _detect_earn_rules_changes(
        self, old_rules: List[Dict], new_rules: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Detect changes in earn_rules (specifically reward_rate changes).
        
        Args:
            old_rules: Old earn rules list
            new_rules: New earn rules list
            
        Returns:
            List of changes detected in earn rules
        """
        changes = []
        
        # Create mappings by category for easier comparison
        old_rules_map = {rule.get("category"): rule for rule in old_rules}
        new_rules_map = {rule.get("category"): rule for rule in new_rules}
        
        # Check all categories in both old and new
        all_categories = set(old_rules_map.keys()) | set(new_rules_map.keys())
        
        for category in all_categories:
            old_rule = old_rules_map.get(category)
            new_rule = new_rules_map.get(category)
            
            old_reward_rate = old_rule.get("reward_rate") if old_rule else None
            new_reward_rate = new_rule.get("reward_rate") if new_rule else None
            
            # Detect reward_rate changes
            if old_reward_rate != new_reward_rate:
                changes.append({
                    "field": f"earn_rules.{category}.reward_rate",
                    "old_value": old_reward_rate,
                    "new_value": new_reward_rate
                })
            
            # Detect reward_unit changes (if applicable)
            old_unit = old_rule.get("reward_unit") if old_rule else None
            new_unit = new_rule.get("reward_unit") if new_rule else None
            
            if old_unit != new_unit:
                changes.append({
                    "field": f"earn_rules.{category}.reward_unit",
                    "old_value": old_unit,
                    "new_value": new_unit
                })
        
        return changes
    
    def track_change(
        self, old_card: Dict[str, Any], new_card: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Track changes from old card to new card and store in history.
        
        Args:
            old_card: Old card JSON
            new_card: New card JSON
            
        Returns:
            Change history entry with card_id, timestamp, and changes
        """
        card_id = new_card.get("card_id")
        if not card_id:
            raise ValueError("New card must have card_id field")
        
        # Detect changes
        changes = self.detect_changes(old_card, new_card)
        
        # Create history entry
        entry = {
            "card_id": card_id,
            "timestamp": datetime.utcnow().isoformat(),
            "changes": changes
        }
        
        # Append to history file
        self._append_to_history(card_id, entry)
        
        return entry
    
    def _append_to_history(self, card_id: str, entry: Dict[str, Any]) -> None:
        """
        Append change entry to history file without overwriting.
        
        Args:
            card_id: Card ID for the history file
            entry: Change entry to append
        """
        history_file = os.path.join(self.history_dir, f"{card_id}.json")
        
        # Load existing history or create new
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []
        
        # Append new entry
        history.append(entry)
        
        # Write back (preserving all history)
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    
    def get_history(self, card_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve full change history for a card.
        
        Args:
            card_id: Card ID
            
        Returns:
            List of all change entries for this card
        """
        history_file = os.path.join(self.history_dir, f"{card_id}.json")
        
        if not os.path.exists(history_file):
            return []
        
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_latest_changes(self, card_id: str) -> Dict[str, Any]:
        """
        Get the most recent change entry for a card.
        
        Args:
            card_id: Card ID
            
        Returns:
            Most recent change entry or empty dict if none exist
        """
        history = self.get_history(card_id)
        return history[-1] if history else {}


# Convenience functions
def track_card_changes(
    old_card: Dict[str, Any], 
    new_card: Dict[str, Any],
    history_dir: str = "backend/data/history"
) -> Dict[str, Any]:
    """
    Convenience function to track changes between two card versions.
    
    Args:
        old_card: Old card JSON
        new_card: New card JSON
        history_dir: Directory for storing history files
        
    Returns:
        Change history entry
    """
    worker = ChangeHistoryWorker(history_dir)
    return worker.track_change(old_card, new_card)


def get_card_history(card_id: str, history_dir: str = "backend/data/history") -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve card change history.
    
    Args:
        card_id: Card ID
        history_dir: Directory where history files are stored
        
    Returns:
        List of all change entries for this card
    """
    worker = ChangeHistoryWorker(history_dir)
    return worker.get_history(card_id)


def get_latest_change(
    card_id: str,
    history_dir: str = "backend/data/history"
) -> Dict[str, Any]:
    """
    Convenience function to retrieve the latest change for a card.

    Args:
        card_id: Card ID
        history_dir: Directory where history files are stored

    Returns:
        Most recent change entry or empty dict if none exist
    """             
    worker = ChangeHistoryWorker(history_dir)
    return worker.get_latest_changes(card_id)
        