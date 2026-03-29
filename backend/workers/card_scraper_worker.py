from datetime import datetime
from typing import Dict, List

from backend.workers.scraper_adapters import GenericBankAdapter, get_supported_sources


class CardScraper:
    def __init__(self):
        self.adapter = GenericBankAdapter()

    def fetch_html(self, source) -> str:
        return self.adapter.fetch_html(source)

    def parse_rewards(self, html: str) -> Dict:
        return self.adapter.parse_rewards(html)

    def parse_fees(self, html: str) -> Dict:
        return self.adapter.parse_fees(html)

    def parse_benefits(self, html: str) -> Dict:
        return self.adapter.parse_benefits(html)

    def normalize_data(self, source_name: str, rewards: Dict, fees: Dict, benefits: Dict) -> Dict:
        def normalize_rate(value):
            if value is None:
                return 0.0
            numeric = float(value)
            return numeric / 100.0 if numeric > 1 else numeric

        return {
            'id': source_name.lower().replace(' ', '_'),
            'bank': source_name,
            'reward_rules': [
                {'category': 'online', 'reward_rate': normalize_rate(rewards.get('online'))},
                {'category': 'dining', 'reward_rate': normalize_rate(rewards.get('dining'))},
                {'category': 'travel', 'reward_rate': normalize_rate(rewards.get('travel'))},
                {'category': 'utilities', 'reward_rate': normalize_rate(rewards.get('utilities'))},
            ],
            'annual_fee': int(fees.get('annual_fee') or 0),
            'joining_fee': int(fees.get('joining_fee') or 0),
            'benefits': {
                'lounge_domestic': int(benefits.get('lounge_domestic') or 0),
                'lounge_international': int(benefits.get('lounge_international') or 0),
                'forex_markup': float(benefits.get('forex_markup') or 0),
                'golf_games': int(benefits.get('golf_games') or 0),
            },
            'last_updated': datetime.utcnow().date().isoformat(),
        }

    def store_postgres(self, normalized_records: List[Dict]) -> Dict:
        # Database write is intentionally abstract in scaffold.
        return {
            'stored_records': len(normalized_records),
            'target': 'postgres',
        }

    def run(self) -> Dict:
        records: List[Dict] = []
        errors: List[str] = []

        for source in get_supported_sources():
            try:
                html = self.fetch_html(source)
                rewards = self.parse_rewards(html)
                fees = self.parse_fees(html)
                benefits = self.parse_benefits(html)
                records.append(self.normalize_data(source.name, rewards, fees, benefits))
            except Exception as error:
                errors.append(f'{source.name}: {error}')

        storage_result = self.store_postgres(records)

        return {
            'status': 'completed',
            'worker': 'card_scraper',
            'timestamp': datetime.utcnow().isoformat(),
            'processed_sources': len(records),
            'errors': errors,
            'storage': storage_result,
        }


def run_card_scrape() -> dict:
    scraper = CardScraper()
    return scraper.run()
