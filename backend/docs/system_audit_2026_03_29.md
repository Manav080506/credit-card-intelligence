# System Audit - 2026-03-29

## Scope
- Data layer, engine layer, API routes, extension integration, delivery readiness.

## Findings (Severity Ordered)

### High
1. Inconsistent card data schemas across datasets and engines.
- Impact: ranking drift and integration friction.
- Recommendation: enforce one canonical contract in API boundary transforms.

2. Multiple comparison implementations with overlapping responsibilities.
- Impact: different endpoints can return conflicting rankings.
- Recommendation: route all compare logic through one deterministic evaluator.

3. Legacy optimizer datasets use flat category fields while newer modules use reward_rates.
- Impact: silent field-mapping bugs likely under expansion.
- Recommendation: add a strict card normalizer shared by optimizer/comparator/predictor.

### Medium
4. ML prediction was classification-oriented previously and not aligned to yearly reward regression target.
- Impact: model outputs were less actionable.
- Recommendation: keep ensemble regression + confidence fallback path.

5. Sparse API contract documentation for public consumers.
- Impact: client integration overhead and versioning risk.
- Recommendation: adopt versioned OpenAPI and contract tests.

6. Confidence score definitions differ by module.
- Impact: dashboard/user trust risk due to inconsistent semantics.
- Recommendation: standardize confidence components and naming.

### Low
7. Prompt and documentation assets exist but need source-of-truth index.
- Impact: maintainability overhead as docs expand.
- Recommendation: add docs index + ownership metadata.

## What Was Added in This Iteration
- Deterministic comparison evaluator with required output fields.
- Ensemble reward prediction model with fallback below confidence 0.65.
- 25-card and 50-card real datasets using normalized reward categories.
- Knowledge graph schema, reward reasoning prompt, extension architecture, public API spec.

## Recommended Structure Ahead
1. Canonical Data Contract
- Card schema v1 under backend/schemas and strict normalizer utility.

2. Single Scoring Path
- compare_cards(cards, monthly_spend) as one source for ranking outputs.

3. Layered Decision Engine
- deterministic scorer first, ML re-ranker second, explainability finalizer third.

4. API Versioning
- /v1 for stable clients; /v2 for experimental ML weighting.

5. UI Confidence Strategy
- display score + components: coverage, stability, category_match.

## Next Actions
1. Add contract tests for dataset and compare output schema.
2. Switch all compare routes to shared evaluator.
3. Add UI panel for confidence component breakdown.
4. Add nightly data QA job for reward-rate anomalies.
