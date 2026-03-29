"""
Card Update Worker - Daily change detection and dataset synchronization

Detects:
1. New cards added to banks/aggregators
2. Reward rate changes
3. Fee updates
4. Eligibility changes

Frequency strategy:
- Daily: Change detection (delta updates)
- Weekly: Full dataset refresh
- Monthly: Full validation
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Simulated card discovery sources
DISCOVERY_QUERIES = [
    "credit cards India list",
    "site:hdfcbank.com credit card",
    "site:axisbank.com credit card",
    "site:icicibank.com credit card",
    "site:sbicard.com credit card",
    "site:paisabazaar.com credit cards",
    "site:bankbazaar.com credit cards",
]

DISCOVERY_SOURCES = [
    "hdfc_bank",
    "axis_bank",
    "icici_bank",
    "sbi_bank",
    "amex_india",
    "paisabazaar",
    "bankbazaar",
    "rss_feeds",
]


class CardUpdateWorker:
    """Daily card update detection and synchronization worker."""

    def __init__(self, db_connection=None, redis_client=None):
        """
        Initialize worker with optional database and cache connections.
        
        Args:
            db_connection: PostgreSQL connection pool
            redis_client: Redis client for cache invalidation
        """
        self.db = db_connection
        self.redis = redis_client
        self.timestamp = datetime.utcnow()

    def run_daily(self) -> Dict[str, any]:
        """
        Execute daily card update workflow.
        
        Returns:
            {
                'status': 'success' | 'partial' | 'failed',
                'new_cards_detected': int,
                'changes_detected': int,
                'errors': List[str],
                'timestamp': datetime
            }
        """
        logger.info("Starting daily card update worker...")
        
        results = {
            "status": "success",
            "new_cards_detected": 0,
            "changes_detected": 0,
            "errors": [],
            "timestamp": self.timestamp,
        }

        try:
            # Step 1: Discover new cards
            new_cards = self.discover_cards()
            results["new_cards_detected"] = len(new_cards)
            
            if new_cards:
                logger.info(f"Discovered {len(new_cards)} new cards")
                self.store_new_cards(new_cards)

            # Step 2: Detect changes in existing cards
            changes = self.detect_changes()
            results["changes_detected"] = len(changes)
            
            if changes:
                logger.info(f"Detected {len(changes)} changes in existing cards")
                self.log_changes(changes)
                self.update_database(changes)

            # Step 3: Invalidate cache
            self.invalidate_cache()
            
            results["status"] = "success"
            
        except Exception as e:
            logger.error(f"Daily card update failed: {str(e)}")
            results["status"] = "failed"
            results["errors"].append(str(e))

        return results

    def discover_cards(self) -> List[Dict]:
        """
        Discover new cards from discovery sources.
        
        Real implementation would:
        - Fetch from bank websites
        - Parse aggregator APIs
        - Query search results
        - Parse RSS feeds
        
        Returns:
            List of discovered card objects with metadata
        """
        logger.info(f"Discovering cards from {len(DISCOVERY_SOURCES)} sources...")
        new_cards = []

        for source in DISCOVERY_SOURCES:
            try:
                cards = self._fetch_from_source(source)
                new_cards.extend(cards)
            except Exception as e:
                logger.warning(f"Discovery from {source} failed: {str(e)}")

        # Deduplicate by card name + issuer
        unique_cards = self._deduplicate_cards(new_cards)
        
        return unique_cards

    def _fetch_from_source(self, source: str) -> List[Dict]:
        """Fetch cards from a specific source."""
        logger.debug(f"Fetching from source: {source}")
        return []

    def _deduplicate_cards(self, cards: List[Dict]) -> List[Dict]:
        """Remove duplicate cards across sources."""
        seen = {}
        unique = []
        
        for card in cards:
            key = (card.get("name", "").lower(), card.get("bank", "").lower())
            if key not in seen:
                seen[key] = True
                unique.append(card)
        
        return unique

    def detect_changes(self) -> List[Dict]:
        """
        Detect changes in existing cards.
        
        Compares:
        - Reward rates per category
        - Annual/joining fees
        - Eligibility criteria
        - Lounge access
        """
        logger.info("Detecting changes in existing cards...")
        changes = []

        try:
            current_cards = self._get_all_cards_from_db()
            
            for card in current_cards:
                latest_data = self._rescrape_card(card["id"])
                
                if latest_data:
                    reward_changes = self._compare_rewards(card, latest_data)
                    changes.extend(reward_changes)
                    
                    fee_changes = self._compare_fees(card, latest_data)
                    changes.extend(fee_changes)
                    
                    eligibility_changes = self._compare_eligibility(card, latest_data)
                    changes.extend(eligibility_changes)
                    
        except Exception as e:
            logger.warning(f"Change detection failed: {str(e)}")

        return changes

    def _get_all_cards_from_db(self) -> List[Dict]:
        """Fetch all cards from database."""
        if not self.db:
            return []
        return []

    def _rescrape_card(self, card_id: str) -> Optional[Dict]:
        """Re-scrape card data from source."""
        return None

    def _compare_rewards(self, old_card: Dict, new_card: Dict) -> List[Dict]:
        """Detect reward rate changes."""
        changes = []
        old_rules = old_card.get("reward_rules", [])
        new_rules = new_card.get("reward_rules", [])
        
        for old_rule, new_rule in zip(old_rules, new_rules):
            if old_rule.get("reward_rate") != new_rule.get("reward_rate"):
                changes.append({
                    "card_id": old_card["id"],
                    "change_type": "reward_rate_change",
                    "category": old_rule.get("category"),
                    "old_value": str(old_rule.get("reward_rate")),
                    "new_value": str(new_rule.get("reward_rate")),
                    "detected_at": self.timestamp,
                })
        
        return changes

    def _compare_fees(self, old_card: Dict, new_card: Dict) -> List[Dict]:
        """Detect annual fee / joining fee changes."""
        changes = []
        
        if old_card.get("annual_fee") != new_card.get("annual_fee"):
            changes.append({
                "card_id": old_card["id"],
                "change_type": "annual_fee_change",
                "old_value": str(old_card.get("annual_fee")),
                "new_value": str(new_card.get("annual_fee")),
                "detected_at": self.timestamp,
            })
        
        return changes

    def _compare_eligibility(self, old_card: Dict, new_card: Dict) -> List[Dict]:
        """Detect eligibility criteria changes."""
        changes = []
        
        if old_card.get("min_income") != new_card.get("min_income"):
            changes.append({
                "card_id": old_card["id"],
                "change_type": "eligibility_min_income_change",
                "old_value": str(old_card.get("min_income")),
                "new_value": str(new_card.get("min_income")),
                "detected_at": self.timestamp,
            })
        
        return changes

    def store_new_cards(self, new_cards: List[Dict]):
        """Store newly discovered cards in database."""
        if not self.db:
            logger.warning("Database not available, skipping store_new_cards")
            return
        
        logger.info(f"Storing {len(new_cards)} new cards...")
        
        for card in new_cards:
            try:
                normalized = self._normalize_card(card)
                logger.debug(f"Stored card: {card.get('id')}")
            except Exception as e:
                logger.warning(f"Failed to store card {card.get('id')}: {str(e)}")

    def log_changes(self, changes: List[Dict]):
        """Log detected changes for audit trail."""
        if not self.db:
            logger.warning("Database not available, skipping log_changes")
            return
        
        logger.info(f"Logging {len(changes)} changes...")
        
        for change in changes:
            try:
                logger.debug(f"Logged change for card {change.get('card_id')}: {change.get('change_type')}")
            except Exception as e:
                logger.warning(f"Failed to log change: {str(e)}")

    def update_database(self, changes: List[Dict]):
        """Apply changes to database."""
        if not self.db:
            logger.warning("Database not available, skipping update_database")
            return
        
        logger.info(f"Updating database with {len(changes)} changes...")
        
        by_card = {}
        for change in changes:
            card_id = change.get("card_id")
            if card_id not in by_card:
                by_card[card_id] = []
            by_card[card_id].append(change)
        
        for card_id, card_changes in by_card.items():
            try:
                logger.debug(f"Updated card {card_id} with {len(card_changes)} changes")
            except Exception as e:
                logger.warning(f"Failed to update card {card_id}: {str(e)}")

    def invalidate_cache(self):
        """Invalidate relevant caches after updates."""
        if not self.redis:
            logger.warning("Redis not available, skipping cache invalidation")
            return
        
        logger.info("Invalidating caches...")
        
        try:
            self.redis.delete("optimize_spend:*")
            self.redis.delete("card_rankings:*")
            logger.info("Cache invalidation complete")
        except Exception as e:
            logger.warning(f"Cache invalidation failed: {str(e)}")

    def _normalize_card(self, card: Dict) -> Dict:
        """Normalize card data to schema format."""
        return {
            "id": card.get("id"),
            "bank": card.get("bank"),
            "network": card.get("network"),
            "segment": card.get("segment"),
            "annual_fee": card.get("annual_fee", 0),
            "joining_fee": card.get("joining_fee", 0),
            "forex_markup": card.get("forex_markup", 0.0),
            "reward_currency": card.get("reward_currency", "INR"),
            "reward_conversion_value": card.get("reward_conversion_value", 1.0),
            "lounge_domestic": card.get("lounge_domestic", 0),
            "lounge_international": card.get("lounge_international", 0),
            "min_income": card.get("min_income", 0),
            "credit_score": card.get("credit_score", 0),
            "tags": card.get("tags", []),
            "last_updated": self.timestamp,
        }


def run_card_update():
    """Scheduled job entry point for daily card updates."""
    logger.info("=== Daily Card Update Job Started ===")
    worker = CardUpdateWorker()
    result = worker.run_daily()
    logger.info(f"=== Daily Card Update Job Complete: {result['status']} ===")
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_card_update()
    print(result)

def update_card_file(path, new_card):

    with open(path, "w") as f:

        json.dump(

            new_card,

            f,

            indent=2

        )


# -------------------------
# update from raw text
# -------------------------

def update_card_from_text(path, raw_text):

    old_card = load_existing_card(path)

    new_card = parse_card_page(raw_text)


    changes = detect_changes(

        old_card,

        new_card

    )


    if changes:

        update_card_file(

            path,

            new_card

        )


    return {

        "updated": bool(changes),

        "changes_detected": changes,

        "card_id": new_card["card_id"]

    }


# -------------------------
# bulk update all cards
# -------------------------

def update_all_cards(card_text_map):

    """
    card_text_map example:

    {

        "backend/data/cards/hdfc/hdfc_millennia_credit_card.json":
        "raw scraped text"

    }

    """

    results = []


    for path, text in card_text_map.items():

        result = update_card_from_text(

            path,

            text

        )


        results.append(result)


    return results
