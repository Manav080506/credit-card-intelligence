# Backend Architecture

## Flow

1. Spend payload enters API route.
2. Feature engineering computes spend ratios and entropy.
3. Recommendation engine scores cards using normalized reward values.
4. Explanation engine generates reason codes and insight summary.
5. Optimizer response includes ranking, confidence, and metadata.

## Modules

- engine/normalizer.py
- engine/feature_engineering.py
- engine/recommendation_engine.py
- engine/explanation_engine.py
- engine/optimizer.py
