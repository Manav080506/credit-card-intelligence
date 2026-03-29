import schedule
import time
import logging

from backend.workers.card_discovery_worker import discover_cards
from backend.workers.reward_refresh_worker import run_reward_refresh
from backend.workers.card_update_worker import run_card_update

logger = logging.getLogger(__name__)


def job():
    """Daily card discovery job."""
    logger.info("Running daily card discovery worker...")
    result = discover_cards()
    logger.info(f"Discovery result: {result}")


def weekly_refresh_job():
    """Weekly reward refresh for full dataset validation."""
    logger.info("Running weekly reward refresh worker...")
    result = run_reward_refresh()
    logger.info(f"Refresh result: {result}")


def daily_update_job():
    """Daily card update job - detect changes in existing cards."""
    logger.info("Running daily card update detection worker...")
    result = run_card_update()
    logger.info(f"Update detection result: {result}")


def run_daily_jobs():
    """Schedule all worker jobs."""
    # Daily discovery at 2 AM
    schedule.every().day.at("02:00").do(job)
    
    # Daily card updates (change detection) at 3 AM
    schedule.every().day.at("03:00").do(daily_update_job)
    
    # Weekly full refresh on Sunday at midnight
    schedule.every().sunday.at("00:00").do(weekly_refresh_job)

    logger.info("Scheduler started...")
    logger.info("Card discovery will run daily at 02:00")
    logger.info("Card update detection will run daily at 03:00")
    logger.info("Reward refresh will run weekly on Sunday at 00:00")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":

    run_daily_jobs()
