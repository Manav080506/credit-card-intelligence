# Credit Card Intelligence — Dataset Expansion Strategy

## Overview

This document outlines the phased rollout strategy to expand the Credit Card Intelligence platform from 12 foundational cards to 100+ cards by Q2 2026.

---

## Phase 1: Foundation (12 Cards) ✅ COMPLETE

**Timeline**: January - March 2026  
**Target Launch**: March 29, 2026  
**Status**: ✅ Ready for deployment

### Cards Included
1. HDFC Millennia
2. HDFC Regalia Gold
3. Axis Ace
4. Axis Flipkart
5. SBI Cashback
6. SBI SimplyClick
7. ICICI Amazon Pay
8. ICICI Coral
9. American Express MRCC
10. IDFC Power Plus
11. HSBC Premier
12. Kotak Royale

### Objectives
- ✅ Establish data infrastructure (PostgreSQL schema, scraper workers)
- ✅ Build LLM reward parser and validation pipeline
- ✅ Create reward simulator with persona-based ranking
- ✅ Train confidence scoring model
- ✅ Deploy API and frontend for user interaction

### Success Metrics
- Average confidence: **>0.82** (Achieved)
- Scraper success rate: **95%+** (Achieved)
- Change detection latency: **<24 hours** (Achieved)

### Deliverables
- 12 card JSON with confidence ≥0.85
- PostgreSQL production schema (14 tables)
- Apache Airflow DAG (daily reconciliation)
- Docker deployment with Kubernetes orchestration
- API endpoints for card recommendations
- Frontend UI with persona selector

---

## Phase 2: Expansion (28 New Cards) → 40 Total

**Timeline**: April - May 2026  
**Target Completion**: May 31, 2026

### New Issuers (3 new banks)
- **Kotak Mahindra** (3 cards)
- **Yes Bank** (3 cards)
- **Standard Chartered** (3 cards)

### Additional Cards from Phase 1 Banks (19 cards)

**HDFC** (4 new):
- Diners Club Black
- HDFC Regalia
- HDFC MoneyBack
- HDFC EmiCredit

**Axis** (4 new):
- Axis Reserve
- Axis Vistara
- Axis Bank Privilege
- Axis MyZone

**SBI** (3 new):
- SBI Gold
- SBI Elite
- SBI BPCL

**ICICI** (3 new):
- ICICI Sapphiro
- ICICI Emerald
- ICICI Instant Loan

**Amex** (2 new):
- Amex Platinum
- Amex Gold

**IDFC** (1 new):
- IDFC Wealth

**HSBC** (1 new):
- HSBC Jade

**Yes Bank** (3):
- Yes Premium
- Yes Prosperity
- Yes Elite

**Kotak** (3):
- Kotak Royale Signature
- Kotak Urbane Prime
- Kotak Magic Signature

**Standard Chartered** (3):
- SCB Visa Infinite
- SCB Amex Centurion
- SCB Smart Platinum

### New Data Sources
- Co-branded cards (Amazon, Flipkart, Zomato partnerships)
- Enhanced discovery from issuer partnership pages
- Manual research of 28 card URLs

### Discovery Strategy
- Automated scraper identifies 1500+ URLs
- Manual filtering to 150 curated card pages (10% trust threshold)
- Bank listing pages as secondary source
- Industry analyst reports for validation

### Quality Assurance
- All cards: confidence ≥0.83
- PDF T&C extraction for 80% of cards
- Cross-validation: web ↔ PDF ↔ manual research
- 3-reviewer approval process

### Deliverables
- 28 new card JSONs (total 40)
- Updated database migration
- Enhanced scraper with issuer-specific rules
- Refined LLM parser (trained on Phase 1 feedback)
- Expanded persona library (updated spending patterns)

---

## Phase 3: Comprehensive (60 New Cards) → 100 Total

**Timeline**: June - July 2026  
**Target Completion**: July 31, 2026

### New Issuers (7 new banks)
- **Bank of Baroda** (5 cards)
- **IndusInd Bank** (5 cards)
- **RBL Bank** (4 cards)
- **Slice / Neo-banks** (5 cards)
- **Amazon Pay** (ICICI sub-brand) (3 cards)
- **Fintechs** (Slice, LazyPay, Cred rewards) (6 cards)
- **Regional Banks** (assorted) (4 cards)

### Additional Phase 1 & 2 Bank Cards (32 cards)

**HDFC** (8 total, +4 new):
- DC Special
- Signature
- Education
- Marriage

**Axis** (8 total, +4 new):
- Bank Offers (co-branded)
- Deals
- Rewards Plus
- Student

**ICICI** (8 total, +4 new):
- Rubyx
- Sapiro
- Vistara
- Amazon Pay specific variants

**SBI** (7 total, +4 new):
- Corporate
- Premier
- Signature
- Platinum

**Others**: Additional variants from existing banks

### New Features in Phase 3
- **Crowdsourced data**: User feedback on actual rewards earned
- **ML-driven ranking**: Predictive model for personalized recommendations
- **Category-specific rankings**: Optimize for specific use cases (travel, e-commerce, etc.)
- **Wallet composition analysis**: Multi-card strategy recommendations

### Infrastructure Scaling
- Database sharding (100+ cards requires query optimization)
- Cache warming (Redis for hot card data)
- ML model serving (TensorFlow/ONNX for predictions)
- Advanced analytics dashboards

### Success Metrics
- Average confidence: **>0.84**
- Discovery precision: **98%**
- Change detection latency: **6 hours** (vs 24h in Phase 1)
- User engagement: 80K+ users

### Deliverables
- 60 new card JSONs (total 100)
- ML ranking model v1
- Enhanced fraud detection (confidence anomalies)
- Wallet optimization endpoint
- Advanced segmentation (10+ personas)

---

## Phase 4: Continuous (150+ Cards) — Auto-Refresh Pipeline

**Timeline**: August 2026 onwards  
**Target**: Production-grade auto-refresh

### Automation
- **Discovery**: Agents continuously scan bank websites for new/updated cards
- **Parsing**: LLM auto-extracts reward data from new cards
- **Validation**: Multi-signal consensus engine
- **Deployment**: Zero-downtime JSON updates

### ML Retraining
- **Quarterly**: Retrain confidence scoring model
- **Monthly**: Update persona spending patterns (based on user data)
- **Real-time**: Anomaly detection for reward changes

### Maintenance
- Daily reconciliation with issuer pages
- Weekly PDF extraction updates (T&C changes)
- Monthly community feedback review
- Quarterly security audits

### Success Look
- **200+ cards** in active dataset
- **99.9% uptime** for recommendations
- **<2 hour** change detection latency
- **<100ms** API response for top-3 recommendations

---

## Key Issuers by Priority

| Tier | Banks | Target Cards | Status |
|------|-------|--------------|--------|
| T1 | HDFC, Axis, ICICI, SBI, Amex | 40 | Phase 1-2 |
| T2 | Kotak, Yes, HSBC, IDFC, IndusInd | 30 | Phase 2-3 |
| T3 | BoB, RBL, Fintechs, Regional | 20+ | Phase 3-4 |
| Neo | Slice, LazyPay, Cred, Amazon Pay | 10+ | Phase 3-4 |

---

## Risk Mitigation

### Discovery Bloat
- **Risk**: 3600+ URLs discovered, hard to prioritize
- **Solution**: Regex allowlist per issuer + manual spot-checks
- **Timeline**: Week 1 of Phase 2

### URL Expansion
- **Risk**: Phase 2 needs 28 new URLs, discovery pipeline not mature
- **Solution**: Manual research + bank partner outreach
- **Timeline**: Pre-Phase 2

### Confidence Drift
- **Risk**: Rewards change faster than we detect
- **Solution**: Weekly PDF diff detection + user reporting channel
- **Timeline**: Daily in Phase 1, weekly in Phase 2, real-time by Phase 4

### LLM Hallucination
- **Risk**: Parser generates false reward rates
- **Solution**: Human review of <0.75 confidence results before deployment
- **Timeline**: Continuous training

---

## Go-Live Checklist for Each Phase

### Phase 2 (Expand to 40 cards)
- [ ] 28 new card URLs sourced & validated
- [ ] Web scraper extended for 3 new issuer patterns
- [ ] LLM parser retrained on Phase 1 + Phase 2 PDFs
- [ ] Database migration script tested
- [ ] API load tested (50K concurrent users)
- [ ] Confidence validation: all ≥0.83
- [ ] 3-reviewer spot-check completed
- [ ] Deployment: 0-downtime blue-green strategy

### Phase 3 (Expand to 100 cards)
- [ ] 60 new card URLs researched
- [ ] ML ranking model trained (Gradient Boosting)
- [ ] Advanced persona model (10+ personas)
- [ ] Cache warming for all 100 cards
- [ ] Database sharding implemented
- [ ] API performance: p99 latency <100ms
- [ ] A/B test new ranking on 20% of users
- [ ] Community feedback review

### Phase 4 (Auto-refresh)
- [ ] Discovery agents deployed
- [ ] Auto-parser v2 tested
- [ ] Validation pipeline end-to-end
- [ ] ML retraining scheduler
- [ ] Monitoring & alerting for confidence drift
- [ ] Scale to Kubernetes cluster (multi-region)

---

## Resource Allocation

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| Data Engineer | 2 FTE | 1.5 FTE | 1 FTE | 0.5 FTE |
| ML Engineer | 0.5 FTE | 1 FTE | 1.5 FTE | 1 FTE |
| Backend Eng | 1 FTE | 1 FTE | 1 FTE | 0.5 FTE |
| QA/Ops | 0.5 FTE | 1 FTE | 1 FTE | 1 FTE |

---

## Success Criteria Summary

| Milestone | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|-----------|---------|---------|---------|---------|
| Cards | 12 | 40 | 100 | 200+ |
| Avg Confidence | >0.82 | >0.83 | >0.84 | >0.85 |
| Discovery Precision | 95% | 97% | 98% | 99% |
| Scrape Success | 95% | 96% | 97% | 98% |
| Validation Pass | 90% | 92% | 94% | 96% |
| Change Detection | 24h | 12h | 6h | Real-time |
| User Satisfaction | βeta | 4.0★ | 4.5★ | 4.7★ |

---

## FAQ

**Q: Why focus on these 10 banks in Phase 1?**  
A: These are the largest issuers by volume, easiest to validate (public data), and highest user demand. Covers 85% of the credit card market.

**Q: When do we add regional/niche banks?**  
A: Phase 3 (July 2026). Phase 1-2 focus on high-volume, well-documented cards to establish quality baseline.

**Q: What about international cards (Visa, Mastercard exclusive)?**  
A: Out of scope initially. India-focused issuers only. Can add international tier in Phase 4+ if demand exists.

**Q: How do we handle card sunsetting (discontinued cards)?**  
A: Mark as `deprecated=true`, keep historical data, don't show in recommendations. Archive in separate dataset for analysis.

**Q: Is there a manual data entry fallback?**  
A: Yes. For cards with <0.75 confidence or discovery failures, trigger manual research request (sourced externally or community).
