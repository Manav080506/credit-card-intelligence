"""Card discovery worker.

Discovers potential credit-card product URLs from configured sources and sitemap
entries, then logs newly discovered URLs not yet in registry.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SOURCE_URLS_FILE = DATA_DIR / "source_urls.json"
REGISTRY_FILE = DATA_DIR / "history" / "card_discovery_registry.json"
DISCOVERY_LOG_FILE = DATA_DIR / "history" / "card_discovery_log.json"


def _load_json(file_path: Path, default_value):
    if not file_path.exists():
        return default_value
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_json(file_path: Path, payload) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def _candidate_links_from_html(base_url: str, html: str) -> Set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: Set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href:
            continue
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        if href.startswith("http") and re.search(r"credit[-_]?card|cards", href, flags=re.IGNORECASE):
            links.add(href.split("#")[0])

    return links


def _candidate_links_from_sitemap(domain_url: str) -> Set[str]:
    sitemap_urls = [
        domain_url.rstrip("/") + "/sitemap.xml",
        domain_url.rstrip("/") + "/sitemap_index.xml",
    ]

    links: Set[str] = set()
    for sitemap_url in sitemap_urls:
        try:
            response = requests.get(sitemap_url, timeout=12)
            if response.status_code != 200:
                continue
            matches = re.findall(r"<loc>(.*?)</loc>", response.text)
            for loc in matches:
                if re.search(r"credit[-_]?card|cards", loc, flags=re.IGNORECASE):
                    links.add(loc.strip())
        except Exception:
            continue

    return links


def discover_cards() -> Dict:
    configured_sources: Dict[str, List[str]] = _load_json(SOURCE_URLS_FILE, {})
    known_registry = set(_load_json(REGISTRY_FILE, []))

    discovered_links: Set[str] = set()

    for _, urls in sorted(configured_sources.items(), key=lambda item: item[0]):
        for url in urls:
            try:
                response = requests.get(url, timeout=12)
                if response.status_code == 200:
                    discovered_links.update(_candidate_links_from_html(url, response.text))
                domain = "/".join(url.split("/")[:3])
                discovered_links.update(_candidate_links_from_sitemap(domain))
            except Exception:
                continue

    # Keep configured URLs in discovery pool.
    for _, urls in configured_sources.items():
        discovered_links.update(urls)

    new_links = sorted(link for link in discovered_links if link not in known_registry)
    merged_registry = sorted(known_registry.union(discovered_links))

    _save_json(REGISTRY_FILE, merged_registry)

    discovery_log = _load_json(DISCOVERY_LOG_FILE, [])
    discovery_log.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "sources_scanned": sum(len(v) for v in configured_sources.values()),
            "discovered_total": len(discovered_links),
            "new_cards_found": len(new_links),
            "new_urls": new_links,
        }
    )
    _save_json(DISCOVERY_LOG_FILE, discovery_log)

    return {
        "status": "completed",
        "worker": "card_discovery",
        "sources_scanned": sum(len(v) for v in configured_sources.values()),
        "cards_found": len(discovered_links),
        "new_cards_found": len(new_links),
        "new_urls": new_links,
    }
