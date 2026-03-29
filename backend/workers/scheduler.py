"""Worker scheduler for daily card refresh pipeline.

Schedule:
- discovery worker -> every 24 hours
- scraper worker -> every 24 hours
- validator -> after scrape
"""

from __future__ import annotations

import logging
import time
from datetime import datetime

from backend.workers.card_discovery_worker import discover_cards
from backend.workers.card_scraper_worker import run_card_scrape
from backend.workers.reward_rules_validator_worker import run_reward_validation


logger = logging.getLogger(__name__)


def run_daily_pipeline() -> dict:
    discovery_result = discover_cards()
    scrape_result = run_card_scrape()
    validation_result = run_reward_validation()

    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "discovery": discovery_result,
        "scrape": scrape_result,
        "validation": validation_result,
        "new_cards_found": discovery_result.get("new_cards_found", 0),
        "cards_updated": validation_result.get("validated_count", 0),
    }

    logger.info("Daily pipeline completed: %s", payload)
    return payload


def start_scheduler() -> None:
    logger.info("Scheduler started. Daily card data pipeline runs every 24 hours.")

    while True:
        run_daily_pipeline()
        time.sleep(24 * 60 * 60)


if __name__ == "__main__":
    run_daily_pipeline()
