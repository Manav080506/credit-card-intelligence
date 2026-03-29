# Production Credit Card Intelligence Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CREDIT CARD DATA PIPELINE SYSTEM                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ INGESTION LAYER                                                              │
├────────────────────────────┬────────────────────────────┬────────────────────┤
│  card_discovery_worker     │   card_scraper_worker      │  pdf_reward_        │
│  - Sitemap discovery       │   - Rate limiting          │  extractor          │
│  - Issuer listing pages    │   - HTML caching           │  - PDF parsing      │
│  - Seed URLs               │   - HTML snapshots         │  - T&C extraction   │
│  - URL deduplication       │   - Issuer-specific        │  - Benefit guides   │
│                            │     extractors             │                     │
│ Output:                    │                            │ Output:            │
│ source_urls.json           │ Output:                    │ extracted_from_     │
│ discovery_registry.json    │ scraped_cards_raw.json     │ pdfs.json           │
│                            │ + html snapshots/          │                     │
└────────────────────────────┴────────────────────────────┴────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ PARSING LAYER                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                    llm_card_parser                                           │
│  - Rule-based regex extraction (primary)                                    │
│  - LLM-assisted category mapping (fallback)                                 │
│  - Milestone interpretation                                                 │
│  - Benefit classification                                                   │
│                                                                              │
│  Output: cards_master_schema.json (canonical truth)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ VALIDATION LAYER                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│              reward_rules_validator_worker                                  │
│  ✓ Reward rate sanity (0-20%)                                               │
│  ✓ Fee consistency checks                                                   │
│  ✓ Cap logic validation                                                     │
│  ✓ Milestone math verification                                              │
│  ✓ Category coverage (≥4 categories)                                        │
│                                                                              │
│  Output: reward_validation_report.json                                      │
│  Status: PASS / FAIL per card                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ CHANGE DETECTION & HISTORY                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│           reward_refresh_worker + change_history_worker                     │
│  - Hash-based page diff detection                                           │
│  - Reward delta computation                                                 │
│  - Timestamped change logging                                               │
│                                                                              │
│  Outputs:                                                                    │
│  - reward_page_hashes.json (snapshot registry)                              │
│  - reward_history/ (change deltas)                                          │
│  - reward_history table (database)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ ENRICHMENT LAYER                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  merchant_classifier          reward_simulator                              │
│  - MCC code mapping            - Annual benefit simulation                  │
│  - Keyword classification      - Persona-based ranking                      │
│  - Training data feedback      - ROI calculation                            │
│                                - Milestone threshold analysis               │
│  Output:                       Output:                                      │
│  merchant_training_data.json   reward_simulation_dataset.json               │
└─────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ DATA STORAGE & SERVING                                                       │
├──────────────────────────────────────────┬──────────────────────────────────┤
│ PostgreSQL (Persistent)                  │ JSON Files (Real-time)           │
│  - credit_cards table                    │  - cards_master_schema.json      │
│  - reward_history (changelog)            │  - cards_optimizer_layer.json    │
│  - scrape_sessions                       │  - cards_metadata_layer.json     │
│  - discovery_registry                    │  - source_urls.json              │
│  - merchant_training_data                │  - target_cards_list.json        │
│  - parsing_confidence_log                │                                  │
│  - reward_simulation_runs                │                                  │
│                                          │                                  │
│  Indexes on:                             │                                  │
│  - bank, network                         │                                  │
│  - data_confidence DESC                  │                                  │
│  - reward_json GIN (JSONB)               │                                  │
└──────────────────────────────────────────┴──────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ API LAYER & CONSUMER                                                         │
├─────────────────────────────────────────┬───────────────────────────────────┤
│  Backend APIs                            │  Frontend Dashboard              │
│  - /optimize-spend                       │  - Top 3 card ranking            │
│  - /compare                              │  - Comparison modal              │
│  - /predict-card                         │  - Card detail drawer           │
│  - /simulate-rewards (new)               │  - Persona selector              │
│                                          │  - Merchant search               │
│  Returns:                                │                                  │
│  - Top 3 ranked cards                    │                                  │
│  - Yearly reward estimates               │                                  │
│  - Confidence scores                     │                                  │
│  - Reasoning                             │                                  │
└─────────────────────────────────────────┴───────────────────────────────────┘
```

## Scheduling & Orchestration

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      APACHE AIRFLOW DAG ORCHESTRATION                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  DAILY (05:00 UTC / 10:30 IST)                                               │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ discover_cards --> scrape_cards --> parse --> validate -->        │       │
│  │ detect_changes --> emit_metrics                                  │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                               │
│  WEEKLY (Monday 02:00 UTC)                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ Full validation pass (strict mode)                               │       │
│  │ Confidence score reweighting                                    │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                               │
│  MONTHLY (1st at 02:00 UTC)                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ Cleanup old HTML snapshots (>90 days)                            │       │
│  │ Archive historical data                                          │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Rate Limiting & Safety

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ RATE LIMITING & COMPLIANCE                                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ • 1–2 sec inter-request delay (REQUEST_DELAY_SEC = 1.5)                     │
│ • Exponential backoff: (1s, 2s, 4s) on retry                                │
│ • Max 3 retries per URL                                                      │
│ • robots.txt pre-flight check                                                │
│ • HTML snapshot caching (24-hour TTL)                                        │
│ • No scraping >48 hrs (unless manual trigger)                                │
│ • User-Agent rotation & identification                                       │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Data Confidence Scoring

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DATA CONFIDENCE MODEL                                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ confidence_score = f(                                                        │
│   extraction_method,     # Web: 0.85, PDF: 0.75, LLM: 0.70                  │
│   category_coverage,     # 0.8 per category defined                         │
│   data_age,              # newer → higher (exponential decay)               │
│   validation_status,     # PASS: +0.10, FAIL: -0.20                        │
│   historical_variance    # low variance → higher confidence                 │
│ )                                                                             │
│                                                                               │
│ Labels:                                                                       │
│  ≥0.85: HIGH CONFIDENCE ✓✓✓                                                 │
│  0.70-0.84: GOOD CONFIDENCE ✓✓                                              │
│  <0.70: NEEDS REVIEW ⚠                                                       │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Database Schema Highlights

### Primary Tables

- **credit_cards**: Master card definitions
- **reward_history**: Change log (JSONB diffs)
- **scrape_sessions**: Pipeline execution log
- **discovery_registry**: URL discovery tracking
- **merchant_training_data**: Classifier training set
- **reward_simulation_runs**: Simulation results cache
- **parsing_confidence_log**: Confidence score tracking

### Indexes
- `idx_credit_cards_bank`, `idx_credit_cards_confidence`
- `idx_reward_json` (GIN JSONB for fast filtering)
- `idx_reward_history_detected_at` (time series)

### Views
- `high_confidence_cards` (confidence ≥ 0.85)
- `recent_reward_changes` (last 30 days)
- `portfolio_coverage_by_issuer` (issuer summary)

## Scalability Considerations

- **Horizontal scaling**: Workers run independently (no shared state)
- **Caching layer**: HTML snapshots stored locally + DB
- **Async expansion**: Framework for parallel workers (reserved for future)
- **Incremental processing**: Only changed cards re-parsed (hash-based)
- **Archive strategy**: Raw HTML purged monthly, JSON retained forever

## Estimated Timelines

```
Phase 1 (COMPLETE):  12 cards,  100% ready      ✓
Phase 2 (IN-PROGRESS):  40 cards, target Apr 2026
Phase 3 (PLANNED):  100+ cards, target Jun 2026
```

## Key Files in This System

```
backend/
├── workers/
│   ├── card_discovery_worker.py
│   ├── card_scraper_worker.py (production grade)
│   ├── llm_card_parser.py
│   ├── pdf_reward_extractor.py (new)
│   ├── reward_rules_validator_worker.py
│   ├── reward_refresh_worker.py
│   └── change_history_worker.py
├── engine/
│   ├── card_comparator.py (ranking logic)
│   ├── merchant_classifier.py (new)
│   ├── reward_simulator.py (new)
│   └── ...
├── airflow/
│   └── dags/
│       └── card_pipeline_dag.py (new)
├── schemas/
│   └── cards_production.sql (new)
├── prompts/
│   └── reward_category_extraction_prompt.txt (new)
└── docs/
    ├── production_scraping_architecture.md (new)
    └── ...
```

---

**Last Updated**: March 29, 2026  
**Status**: Production architecture ready for 40–100 card roadmap  
**Next Milestone**: Deploy Phase 2 (40 cards) with full confidence scoring
