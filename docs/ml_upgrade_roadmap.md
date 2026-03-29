# ML Upgrade Roadmap

## Phase 1: Rule-Based Engine

- Deterministic formula scoring.
- Explainable recommendation outputs.

## Phase 2: ML Recommendation

- Input features: spend ratios, spend variance, annual fee, reward rates.
- Labels: historical best card outcomes and user acceptance.
- Candidate models: RandomForest, XGBoost, LightGBM.
- Output: top 3 cards with confidence.

## Phase 3: Reinforcement Loop

- Feedback events: card selected, recommendation skipped, spend changes.
- Objective: maximize long-term yearly value and user retention.

## Phase 4: Personalization Graph AI

- Segment users into cohorts: students, travelers, freelancers, high spenders.
- Learn cluster-specific card ranking policies.
