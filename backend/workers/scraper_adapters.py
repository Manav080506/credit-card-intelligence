from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ScraperSource:
    name: str
    url: str
    source_type: str


class BaseScraperAdapter:
    def fetch_html(self, source: ScraperSource) -> str:
        raise NotImplementedError

    def parse_rewards(self, html: str) -> Dict:
        raise NotImplementedError

    def parse_fees(self, html: str) -> Dict:
        raise NotImplementedError

    def parse_benefits(self, html: str) -> Dict:
        raise NotImplementedError


class GenericBankAdapter(BaseScraperAdapter):
    def fetch_html(self, source: ScraperSource) -> str:
        # Network call intentionally omitted in scaffold.
        return f"<html><title>{source.name}</title></html>"

    def parse_rewards(self, html: str) -> Dict:
        return {
            'online': None,
            'dining': None,
            'travel': None,
            'utilities': None,
        }

    def parse_fees(self, html: str) -> Dict:
        return {
            'annual_fee': None,
            'joining_fee': None,
        }

    def parse_benefits(self, html: str) -> Dict:
        return {
            'lounge_domestic': None,
            'lounge_international': None,
            'forex_markup': None,
            'golf_games': None,
        }


def get_supported_sources() -> List[ScraperSource]:
    return [
        ScraperSource('HDFC', 'https://www.hdfcbank.com/personal/pay/cards/credit-cards', 'bank'),
        ScraperSource('ICICI', 'https://www.icicibank.com/personal-banking/cards/credit-card', 'bank'),
        ScraperSource('Axis', 'https://www.axisbank.com/retail/cards/credit-card', 'bank'),
        ScraperSource('SBI', 'https://www.sbicard.com/en/personal/credit-cards.page', 'bank'),
        ScraperSource('HSBC', 'https://www.hsbc.co.in/credit-cards/', 'bank'),
        ScraperSource('Amex', 'https://www.americanexpress.com/en-in/credit-cards/', 'bank'),
        ScraperSource('Paisabazaar', 'https://www.paisabazaar.com/credit-card/', 'aggregator'),
        ScraperSource('BankBazaar', 'https://www.bankbazaar.com/credit-card.html', 'aggregator'),
        ScraperSource('CardInsider', 'https://cardinsider.com/', 'aggregator'),
        ScraperSource('Wishfin', 'https://www.wishfin.com/credit-card/', 'aggregator'),
    ]
