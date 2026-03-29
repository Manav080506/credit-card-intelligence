# Production Scraping Architecture

## Goal

Maintain continuously updated, high-confidence credit card reward dataset for real-time optimization.

---

## Design Principles

- **Deterministic outputs**: Same input → same structured output
- **Reproducible calculations**: Reward math auditable and verifiable
- **Auditable change history**: All reward deltas tracked with timestamp
- **Modular workers**: Each stage independent, testable, replaceable
- **LLM as enhancement layer**: Rule-based extraction first, LLM only for ambiguity

---

## Architecture Layers

### DATA SOURCES

**Primary sources:**
- Official bank credit card pages
- Fintech aggregators (CreditWise, Mint, GetMoneySmart)
- PDF T&Cs and benefit guides
- Official reward T&C pages (bank Ts&Cs portals)

**Covered issuers (expanding):**
- HDFC, Axis, SBI, ICICI, AmEx, IDFC, HSBC, Standard Chartered, Yes Bank, Kotak

---

### INGESTION LAYER (`card_discovery_worker`)

**Responsibility**: Discover new card URLs and maintain master source registry

**Methods:**
1. Sitemap parsing (`/sitemap.xml` discovery)
2. Issuer listing pages (credit card category pages)
3. Manual seed URLs (`source_urls.json`)
4. Fintech aggregator scraping

**Constraints:**
- Strict URL allowlist per issuer (no crawl bloat)
- Regex filters to isolate card product pages
- Deduplication by canonical URL

**Outputs:**
- `source_urls.json` — master source registry
- `card_discovery_registry.json` — discovered URLs with metadata

---

### SCRAPING LAYER (`card_scraper_worker`)

**Responsibility**: Download HTML and extract structured text sections

**Fields extracted:**
1. Reward text (fees, earning rates, categories)
2. Milestone benefits (bonus cashback at thresholds)
3. Annual/joining fees
4. Benefits (lounge, travel insurance, etc.)
5. Caps and exclusions

**Storage:**
- Raw HTML snapshots: `data/raw_html/{bank}/{card_id}.html`
- Extracted sections: `data/raw_json/{bank}/{card_id}.json`

**Safety:**
- Rate limiting (1–2 sec per request)
- Respect `robots.txt`
- Retry with exponential backoff
- Cache hits to avoid re-download

---

### PARSING LAYER (`llm_card_parser`)

**Responsibility**: Convert raw text into schema-compliant JSON

**Rule-based first:**
- Regex extraction for standard patterns (e.g., "5% cashback on X")
- Direct keyword mapping for known categories
- Numeric parsing for fees and caps

**LLM-assisted (fallback):**
- Category disambiguation ("dining" vs "restaurants" vs "food")
- Milestone interpretation ("quarterly milestone at ₹5L spend")
- Benefit classification (insurance type, lounge provider)

**Output format**: Compliant with `card_reward_schema.json`

---

### VALIDATION LAYER (`reward_rules_validator_worker`)

**Checks:**
- **Reward rate sanity**: 0 ≤ rate ≤ 0.20 (no >20% cashback without exclusion)
- **Fee consistency**: annual_fee ≥ joining_fee
- **Cap logic**: cap_limit ≥ threshold
- **Milestone math**: bonus ≤ (annual_spend - threshold) × rate
- **Category coverage**: ≥ 4 categories defined (travel, dining, shopping, utilities, groceries, fuel)

**Output**: `reward_validation_report.json` with pass/fail per card

---

### CHANGE DETECTION (`reward_refresh_worker`)

**Responsibility**: Identify reward changes between versions

**Logic:**
1. Hash current page snapshot
2. Compare to stored hash (previous scrape)
3. If diff detected, parse new reward structure
4. Compute delta (JSON diff)
5. Store in history

**Outputs:**
- `reward_page_hashes.json` — previous snapshot hashes
- `reward_history/` — timestamped deltas per card

---

### DATA STORAGE LAYERS

**Layer 1: Raw data**
- `data/raw_html/{bank}/` — archived HTML
- `data/raw_json/{bank}/` — extracted sections

**Layer 2: Validated data**
- `cards_master_schema.json` — canonical truth (all cards, all fields)
- `cards_optimizer_layer.json` — reward rates + fees for ranking
- `cards_metadata_layer.json` — names, images, issuer metadata

**Layer 3: Production database**
- PostgreSQL `credit_cards` table (JSONB reward/benefit fields)
- `reward_history` changelog

---

### SCHEDULING (`scheduler.py`)

**Daily (5 AM IST):**
- Run change detection on all registered URLs
- Scrape & parse only changed cards
- Log deltas

**Weekly (Monday 2 AM IST):**
- Full re-parse and validation of all ≥10% confidence cards
- Regenerate optimizer layer

**Monthly (1st, 2 AM IST):**
- Manual verification pass
- Purge outdated raw HTML
- Confidence score reweight

---

### OBSERVABILITY

**Metrics tracked:**
- `cards_discovered` — new URLs found this cycle
- `cards_scraped` — success count
- `cards_failed` — failures (reason, URL)
- `parse_confidence_avg` — average data_confidence score
- `coverage_percent` — % of target issuer portfolio covered
- `change_frequency_avg` — median days between reward updates per card

**Dashboards:**
- Real-time scrape health
- Coverage % by issuer
- Historical confidence trends

---

### SAFETY & COMPLIANCE

- **Rate limiting**: 1–2 sec inter-request delay
- **robots.txt** compliance: check before scraping each domain
- **Local caching**: Store HTML to avoid re-downloads
- **Frequency caps**: Max once per 48 hrs per card (unless manual trigger)
- **User-Agent rotation**: Identify as legitimate bot
- **Error recovery**: Exponential backoff, max 3 retries per URL
- **Data freshness**: Flag confidence down if stale (>30 days old)

---

## Target Card Portfolio

**Phase 1 (current):** 12 cards (validation)
**Phase 2:** 40 cards (quality iteration)
**Phase 3 (production):** 100+ cards across 10 issuers

See `target_cards_list.json` for full roadmap.

---

## Example Flow

```
source_urls.json (seed)
        ↓
discovery_worker
        ↓
raw_html/ (cached snapshots)
        ↓
scraper_worker
        ↓
raw_json/ (extracted sections)
        ↓
llm_card_parser
        ↓
intermediate schema
        ↓
reward_rules_validator_worker
        ↓
cards_master_schema.json (canonical truth)
        ↓
cards_optimizer_layer.json (ready for ranking)
        ↓
Dashboard & API consume
```

---

## Next Steps

1. Expand source URLs for all 10 issuers
2. Implement issuer-specific scrapers (HTML structure differs)
3. Build PDF extractor for benefit guides
4. Train confidence scoring on real data variance
5. Deploy to production database + Airflow scheduler
