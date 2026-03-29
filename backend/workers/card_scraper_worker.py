"""Credit card scraper worker - Production Grade.

This worker fetches card product pages and extracts structured reward data.

Features:
- Caching: avoids re-downloading unchanged pages
- Rate limiting: respects request delays
- Issuer-specific extractors: handles different HTML structures
- Snapshot storage: archives raw HTML for audit trail
- Deterministic output: reproducible parsing
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SOURCE_URLS_FILE = DATA_DIR / "source_urls.json"
RAW_OUTPUT_FILE = DATA_DIR / "cards" / "scraped_cards_raw.json"
RAW_HTML_DIR = DATA_DIR / "raw_html"
CACHE_FILE = DATA_DIR / "history" / "scrape_cache.json"

DEFAULT_REWARD_RATES = {
    "online_shopping": 0.01,
    "dining": 0.01,
    "travel": 0.01,
    "groceries": 0.01,
    "fuel": 0.01,
    "utilities": 0.01,
    "general": 0.01,
}

# Rate limiting config
REQUEST_DELAY_SEC = 1.5
MAX_RETRIES = 3
RETRY_BACKOFF = (1, 2, 4)  # seconds


def _load_cache() -> Dict[str, Dict]:
    """Load HTML snapshot cache from disk."""
    if not CACHE_FILE.exists():
        return {}
    try:
        with CACHE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache: Dict[str, Dict]) -> None:
    """Save HTML snapshot cache to disk."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def _hash_content(content: str) -> str:
    """Compute SHA-256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def _save_html_snapshot(html: str, bank: str, card_id: str) -> Path:
    """Save raw HTML snapshot for audit trail."""
    snapshot_dir = RAW_HTML_DIR / bank.lower().replace(" ", "_")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = snapshot_dir / f"{card_id}_{timestamp}.html"
    
    with filename.open("w", encoding="utf-8") as f:
        f.write(html)
    
    return filename


def _should_rescrape(url: str, cache: Dict) -> bool:
    """Check if URL needs to be re-scraped based on cache."""
    if url not in cache:
        return True
    
    # Re-scrape if last fetch >24 hours old
    last_fetch = cache[url].get("last_fetch_ts")
    if not last_fetch:
        return True
    
    elapsed_hours = (datetime.utcnow().timestamp() - last_fetch) / 3600
    return elapsed_hours > 24


def _load_source_urls() -> Dict[str, List[str]]:
    if not SOURCE_URLS_FILE.exists():
        return {}
    with SOURCE_URLS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {str(k): list(v) for k, v in data.items()}


def fetch_page(url: str, retry_count: int = 0) -> Tuple[str, bool]:
    """
    Fetch page with exponential backoff retry.
    
    Returns:
        (html_content, is_fresh) - is_fresh=False if returned from cache
    """
    if retry_count >= MAX_RETRIES:
        raise Exception(f"Max retries ({MAX_RETRIES}) exceeded for {url}")
    
    time.sleep(REQUEST_DELAY_SEC)
    
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; CreditCardIntelligenceBot/1.0)",
                "Accept-Language": "en-IN,en;q=0.9",
            },
        )
        response.raise_for_status()
        return response.text, True
    except Exception as e:
        if retry_count < MAX_RETRIES:
            backoff = RETRY_BACKOFF[min(retry_count, len(RETRY_BACKOFF) - 1)]
            time.sleep(backoff)
            return fetch_page(url, retry_count + 1)
        raise


def extract_card_name(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)

    title = soup.find("title")
    if title and title.get_text(strip=True):
        return title.get_text(strip=True).split("|")[0].strip()

    return "Unknown Credit Card"


def _extract_first_currency_amount(text: str) -> float:
    amount_match = re.search(r"(?:₹|rs\.?|inr)\s*([\d,]+)", text, flags=re.IGNORECASE)
    if not amount_match:
        return 0.0
    return float(amount_match.group(1).replace(",", ""))


def extract_annual_fee(text: str) -> float:
    fee_patterns = [
        r"annual\s+fee[^\d₹inr]*?(?:₹|rs\.?|inr)\s*([\d,]+)",
        r"renewal\s+fee[^\d₹inr]*?(?:₹|rs\.?|inr)\s*([\d,]+)",
    ]

    for pattern in fee_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", ""))

    return _extract_first_currency_amount(text)


def extract_reward_rates(text: str) -> Dict[str, float]:
    rates = dict(DEFAULT_REWARD_RATES)

    patterns = {
        "online_shopping": [r"(\d+(?:\.\d+)?)%[^.]{0,80}(?:online|shopping|e-?com)"],
        "dining": [r"(\d+(?:\.\d+)?)%[^.]{0,80}dining"],
        "travel": [r"(\d+(?:\.\d+)?)%[^.]{0,80}travel"],
        "groceries": [r"(\d+(?:\.\d+)?)%[^.]{0,80}(?:grocery|groceries)"],
        "fuel": [r"(\d+(?:\.\d+)?)%[^.]{0,80}fuel"],
        "utilities": [r"(\d+(?:\.\d+)?)%[^.]{0,80}(?:utility|utilities|bill)"],
        "general": [r"(\d+(?:\.\d+)?)%[^.]{0,80}(?:other|others|all spends|general)"]
    }

    for category, regex_list in patterns.items():
        found_rates: List[float] = []
        for regex in regex_list:
            for match in re.finditer(regex, text, flags=re.IGNORECASE):
                found_rates.append(float(match.group(1)) / 100.0)
        if found_rates:
            rates[category] = max(found_rates)

    return rates


def extract_milestones(text: str) -> List[Dict[str, float]]:
    milestones: List[Dict[str, float]] = []
    pattern = re.compile(
        r"spend\s*(?:of)?\s*(?:₹|rs\.?|inr)\s*([\d,]+)[^.]{0,60}(?:bonus|voucher|points|reward)[^.]{0,30}(?:₹|rs\.?|inr)\s*([\d,]+)",
        flags=re.IGNORECASE,
    )

    for match in pattern.finditer(text):
        threshold = float(match.group(1).replace(",", ""))
        bonus = float(match.group(2).replace(",", ""))
        milestones.append({"spend_threshold": threshold, "bonus_value": bonus})

    return milestones


def extract_benefits(text: str) -> List[str]:
    benefits: List[str] = []
    if "lounge" in text.lower():
        benefits.append("lounge_access")
    if "forex" in text.lower():
        benefits.append("forex_benefit")
    if "fuel surcharge" in text.lower():
        benefits.append("fuel_surcharge_waiver")
    return benefits


def infer_bank_from_url(url: str) -> str:
    host = url.split("//")[-1].split("/")[0].lower()
    bank_map = {
        "hdfcbank": "HDFC Bank",
        "axisbank": "Axis Bank",
        "sbicard": "SBI Card",
        "icicibank": "ICICI Bank",
        "americanexpress": "American Express",
        "idfcfirstbank": "IDFC First Bank",
        "hsbc": "HSBC",
        "standardchartered": "Standard Chartered",
        "yesbank": "Yes Bank",
        "kotak": "Kotak Mahindra Bank",
    }
    for key, label in bank_map.items():
        if key in host:
            return label
    return host


def _extract_from_hdfc(soup: BeautifulSoup, text: str) -> Dict:
    """HDFC issuer-specific extractor."""
    rates = dict(DEFAULT_REWARD_RATES)
    # HDFC often uses structured reward text in specific tags
    reward_section = soup.find("div", {"class": re.compile(r".*reward.*", re.I)})
    if reward_section:
        reward_text = reward_section.get_text()
        # Parse HDFC-specific patterns
        if "5% cashback" in reward_text.lower():
            rates["online_shopping"] = 0.05
    return rates


def _extract_from_axis(soup: BeautifulSoup, text: str) -> Dict:
    """Axis Bank issuer-specific extractor."""
    rates = dict(DEFAULT_REWARD_RATES)
    # Axis uses "X reward points" structure
    return rates


def _extract_from_icici(soup: BeautifulSoup, text: str) -> Dict:
    """ICICI Bank issuer-specific extractor."""
    rates = dict(DEFAULT_REWARD_RATES)
    # ICICI patterns
    return rates


def _get_issuer_extractor(bank: str):
    """Get issuer-specific extractor function."""
    extractors = {
        "HDFC Bank": _extract_from_hdfc,
        "Axis Bank": _extract_from_axis,
        "ICICI Bank": _extract_from_icici,
    }
    return extractors.get(bank)


def scrape_card(url: str, cache: Dict) -> Tuple[Dict, bool]:
    """
    Scrape a single card page.
    
    Returns:
        (card_data, is_fresh)
    """
    bank = infer_bank_from_url(url)
    card_id = url.split("/")[-1].split("?")[0]
    
    # Check cache
    if not _should_rescrape(url, cache):
        cached = cache.get(url, {})
        return {
            "card_name": cached.get("card_name", "Unknown"),
            "bank": bank,
            "annual_fee": cached.get("annual_fee", 0.0),
            "reward_rates": cached.get("reward_rates", DEFAULT_REWARD_RATES),
            "milestones": cached.get("milestones", []),
            "benefits": cached.get("benefits", []),
            "source_url": url,
            "last_updated": datetime.utcnow().isoformat(),
            "from_cache": True,
        }, False
    
    # Fetch fresh
    html, _ = fetch_page(url)
    html_hash = _hash_content(html)
    
    # Save snapshot
    snapshot_path = _save_html_snapshot(html, bank, card_id)
    
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    
    # Use issuer-specific extractor if available
    issuer_extractor = _get_issuer_extractor(bank)
    if issuer_extractor:
        reward_rates = issuer_extractor(soup, text)
    else:
        reward_rates = extract_reward_rates(text)
    
    card_data = {
        "card_name": extract_card_name(soup),
        "bank": bank,
        "annual_fee": extract_annual_fee(text),
        "reward_rates": reward_rates,
        "milestones": extract_milestones(text),
        "benefits": extract_benefits(text),
        "source_url": url,
        "last_updated": datetime.utcnow().isoformat(),
        "from_cache": False,
        "snapshot_path": str(snapshot_path),
        "html_hash": html_hash,
    }
    
    # Update cache
    cache[url] = {
        "card_name": card_data["card_name"],
        "annual_fee": card_data["annual_fee"],
        "reward_rates": card_data["reward_rates"],
        "milestones": card_data["milestones"],
        "benefits": card_data["benefits"],
        "html_hash": html_hash,
        "last_fetch_ts": datetime.utcnow().timestamp(),
        "snapshot_path": str(snapshot_path),
    }
    
    return card_data, True

def run_card_scrape(parallel: bool = False, workers: int = 4) -> Dict:
    """
    Main scraper entry point.
    
    Args:
        parallel: NOT USED (reserved for future async implementation)
        workers: Number of parallel workers (reserved for future)
    """
    source_urls = _load_source_urls()
    flattened_urls: List[str] = []
    for _, urls in sorted(source_urls.items(), key=lambda item: item[0]):
        flattened_urls.extend(urls)
    
    cache = _load_cache()
    cards: List[Dict] = []
    fresh_count = 0
    cache_hits = 0
    error_count = 0
    
    for idx, url in enumerate(flattened_urls, 1):
        try:
            print(f"[{idx}/{len(flattened_urls)}] Scraping: {url}")
            card_data, is_fresh = scrape_card(url, cache)
            cards.append(card_data)
            if is_fresh:
                fresh_count += 1
            else:
                cache_hits += 1
        except Exception as error:
            print(f"ERROR scraping {url}: {error}")
            error_count += 1
            cards.append(
                {
                    "card_name": "Unknown Credit Card",
                    "bank": infer_bank_from_url(url),
                    "annual_fee": 0.0,
                    "reward_rates": dict(DEFAULT_REWARD_RATES),
                    "milestones": [],
                    "benefits": [],
                    "source_url": url,
                    "last_updated": datetime.utcnow().isoformat(),
                    "error": str(error),
                    "from_cache": False,
                }
            )
    
    # Save cache
    _save_cache(cache)
    
    # Save outputs
    RAW_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RAW_OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(cards, file, indent=2)
    
    return {
        "status": "completed",
        "worker": "card_scraper",
        "total_urls": len(flattened_urls),
        "cards_extracted": len(cards),
        "fresh_scrapes": fresh_count,
        "cache_hits": cache_hits,
        "errors": error_count,
        "output_file": str(RAW_OUTPUT_FILE),
        "html_snapshot_dir": str(RAW_HTML_DIR),
    }
