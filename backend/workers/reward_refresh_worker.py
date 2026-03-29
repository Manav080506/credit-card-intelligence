"""Reward refresh worker.

Performs hash-based change detection and triggers re-scrape when source pages
change.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from urllib.request import Request, urlopen

from backend.workers.card_scraper_worker import run_card_scrape


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SOURCE_URLS_FILE = DATA_DIR / "source_urls.json"
HASH_CACHE_FILE = DATA_DIR / "history" / "reward_page_hashes.json"
REFRESH_LOG_FILE = DATA_DIR / "history" / "reward_refresh_log.json"


def hash_content(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _load_json(file_path: Path, default_value):
    if not file_path.exists():
        return default_value
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_json(file_path: Path, payload) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def _flatten_sources() -> List[str]:
    data = _load_json(SOURCE_URLS_FILE, {})
    urls: List[str] = []
    for _, source_urls in sorted(data.items(), key=lambda item: item[0]):
        urls.extend(source_urls)
    return urls


def run_reward_refresh() -> Dict:
    urls = _flatten_sources()
    old_hashes = _load_json(HASH_CACHE_FILE, {})
    new_hashes: Dict[str, str] = {}
    changed_urls: List[str] = []

    for url in urls:
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; CreditCardIntelligenceBot/1.0)",
                    "Accept-Language": "en-IN,en;q=0.9",
                },
            )
            with urlopen(request, timeout=15) as response:
                raw = response.read().decode("utf-8", errors="ignore")
            new_hash = hash_content(raw)
            new_hashes[url] = new_hash
            if old_hashes.get(url) != new_hash:
                changed_urls.append(url)
        except Exception:
            continue

    _save_json(HASH_CACHE_FILE, new_hashes)

    scrape_result = None
    if changed_urls:
        scrape_result = run_card_scrape()

    log = _load_json(REFRESH_LOG_FILE, [])
    log.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "total_urls": len(urls),
            "changed_urls": len(changed_urls),
            "changed_url_list": changed_urls,
            "scrape_triggered": bool(changed_urls),
        }
    )
    _save_json(REFRESH_LOG_FILE, log)

    return {
        "status": "completed",
        "worker": "reward_refresh",
        "total_urls": len(urls),
        "changed_urls": len(changed_urls),
        "scrape_triggered": bool(changed_urls),
        "scrape_result": scrape_result,
    }
