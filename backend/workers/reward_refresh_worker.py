from datetime import datetime

from backend.workers.card_scraper_worker import run_card_scrape


WEEKLY_CRON = "0 0 * * 0"


def run_reward_refresh() -> dict:
    scrape_result = run_card_scrape()
    return {
        'status': 'completed',
        'worker': 'reward_refresh',
        'timestamp': datetime.utcnow().isoformat(),
        'schedule': WEEKLY_CRON,
        'scrape_result': scrape_result,
    }
