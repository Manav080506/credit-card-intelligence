# Credit Card Intelligence Platform — Architecture

## System Overview

```
                          ┌─────────────────────┐
                          │   USER INPUT        │
                          ├─────────────────────┤
                          │ • Monthly spend     │
                          │ • Persona           │
                          │ • Wallet cards      │
                          │ • Goals             │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
        ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
        │  FEATURE ENG    │  │ REWARD NORM  │  │  OPTIMIZER   │
        │                 │  │              │  │              │
        │ • Normalize     │  │ • Decay old  │  │ • Rank by ~  │
        │   spend data    │  │   rewards    │  │   net benefit│
        │ • MCC classify  │  │ • Weight     │  │ • Score risk │
        │ • Merchant map  │  │   current    │  │ • Validate   │
        │ • Category infer│  │                │  │   feasibility│
        └────────┬────────┘  └──────┬───────┘  └──────┬───────┘
                 │                  │                 │
                 └──────────────────┼─────────────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
         ┌─────────────────────┐        ┌──────────────────────┐
         │ CONFIDENCE ENGINE   │        │ EXPLANATION ENGINE   │
         │                     │        │                      │
         │ • Cross-validate    │        │ • Top 3 cards        │
         │   multiple signals  │        │ • Yearly savings     │
         │ • Aggregate PDF +   │        │ • Why each card      │
         │   web scrapers      │        │ • Alternative rank   │
         │ • Track drift       │        │ • Risk warnings      │
         └──────────┬──────────┘        └──────────┬───────────┘
                    │                             │
                    └─────────────────┬───────────┘
                                      │
                    ┌─────────────────┴──────────────────┐
                    │                                    │
                    ▼                                    ▼
         ┌─────────────────────┐        ┌──────────────────────┐
         │   RECOMMENDATION    │        │   AUDIT & LOGGING    │
         │                     │        │                      │
         │ ✓ Top 3 cards       │        │ • All inputs logged  │
         │ ✓ Annual savings    │        │ • Score history      │
         │ ✓ Confidence score  │        │ • Change tracking    │
         │ ✓ Detailed explain  │        │ • Version control    │
         └─────────────────────┘        └──────────────────────┘
```

## Data Pipeline (Continuous)

```
┌──────────────────────────────────────────────────────────────┐
│              SCRAPING & EXTRACTION WORKERS                    │
│                                                               │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐   │
│  │ Card Discovery  │  │ Web Scrapers │  │ PDF & T&C     │   │
│  │ (3600 URLs)     │  │ (HTML parse) │  │ Extractors    │   │
│  │                 │  │              │  │               │   │
│  │ → Dedupe        │  │ → Issuer-    │  │ → Multi-page  │   │
│  │ → Validate      │  │   specific   │  │   parsing     │   │
│  │ → Rank by trust │  │   rules      │  │ → Confidence  │   │
│  │                 │  │ → Cache 24h  │  │   scoring     │   │
│  └────────┬────────┘  └──────┬───────┘  └───────┬───────┘   │
│           │                  │                  │             │
│           └──────────────────┼──────────────────┘             │
│                              │                                 │
└──────────────────────────────┼──────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌──────────────────────┐      ┌───────────────────────┐
    │ LLM REWARD PARSER    │      │ REWARD VALIDATOR      │
    │                      │      │                       │
    │ • Extract rates      │      │ • Cross-check         │
    │ • Categorize         │      │   web ↔ PDF          │
    │ • Confidence score   │      │ • Outlier detection   │
    │                      │      │ • Trend analysis      │
    └──────────┬───────────┘      └───────────┬───────────┘
               │                              │
               │              ┌───────────────┘
               │              │
               └──────────────┼────────────────┐
                              │                │
                    ┌─────────▼──────────┐    │
                    │\                   │    │
                    │ DATABASE (PostgreSQL)   │
                    │                   |    │
                    │ • credit_cards    │    │
                    │ • reward_history  │    │
                    │ • scrape_sessions │    │
                    │ • parsing_logs    │    │
                    │ • confidence_log  │    │
                    └───────────────────┘    │
                                             │
                              ┌──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ REWARD SIMULATOR │
                    │                  │
                    │ 5 Personas:      │
                    │ • High earner    │
                    │ • Online shopper │
                    │ • Family         │
                    │ • Minimalist     │
                    │ • Traveler       │
                    │                  │
                    │ → Annual ROI     │
                    │ → Ranking        │
                    └──────────────────┘
```

## Database Schema (14 Tables)

### Core Tables
- **credit_cards**: Card metadata + JSONB reward/benefit fields (indexes: bank, issuer, searchable)
- **reward_history**: Timestamped reward deltas (JSONB + changelog)
- **reward_simulation_runs**: Pre-calculated persona simulations

### Operational
- **scrape_sessions**: Audit trail, rate limit tracking, retry history
- **discovery_registry**: Source URLs, trust scores, discovery order
- **merchant_training_data**: Feedback loop for classifier improvements

### Quality
- **parsing_confidence_log**: Per-field confidence scores, cross-method agreement
- **change_detection_log**: HTML snapshot hashes (detects rewards changes)
- **validation_failures**: Rejected rewards (for investigation)

### Materialized Views
- `high_confidence_cards` (≥0.85 confidence)
- `recent_reward_changes` (30-day deltas)
- `portfolio_coverage_by_issuer` (for gap analysis)

## Scaling Phases

### Phase 1: Foundation (12 cards) ✅
- HDFC Millennia, Regalia
- Axis Ace, Flipkart
- SBI Cashback, SimplyClick
- ICICI Amazon Pay, Coral
- Amex MRCC, IDFC Power Plus, HSBC Premier, Kotak Royale

### Phase 2: Expansion (28 new cards) — April 2026
- Secondary HDFC, Axis, ICICI, SBI variants
- Co-branded partnership cards (Amazon, Flipkart, Zomato)
- Niche cards (golf, premium, store-specific)

### Phase 3: Comprehensive (60 new cards) — June 2026
- All major issuers across segments
- Regional bank partnerships
- Fintech & neo-bank cards

### Phase 4: AutoRefresh (unlimited) — August 2026
- Continuous pipeline
- ML-driven URL discovery
- Quarterly model retraining

## Success Metrics

| Metric | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|
| Cards | 12 | 40 | 100 |
| Avg Confidence | >0.82 | >0.83 | >0.84 |
| Discovery Precision | 95% | 97% | 98% |
| Scrape Success Rate | 95% | 96% | 97% |
| Validation Pass Rate | 90% | 92% | 94% |
| Change Detection Latency | 24h | 12h | 6h |

## Deployment

```
┌─────────────────────────────────────────────┐
│  Docker Containers (Kubernetes)             │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Scraper  │  │ LLM      │  │ API      │  │
│  │ Workers  │  │ Parser   │  │ Server   │  │
│  │ (2x)     │  │ (1x)     │  │ (3x)     │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ PostgreSQL (Managed, with backup)   │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Airflow (scheduler) — Daily          │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Key Design Decisions

1. **Rate Limiting**: 1.5s inter-request + exponential backoff
2. **Caching**: 24h HTML cache (reduces redundant fetches by 70%)
3. **Confidence**: Multi-signal weighted scoring (web + PDF + LLM agreement)
4. **Isolation**: Issuer-specific extractors (handles HTML variations)
5. **Auditability**: SHA-256 snapshots enable root-cause analysis for changes
