# Next Logical Build Steps

## Priority Order (Tomorrow)

1. Improve dataset quality (expand and verify 50 -> 200 cards).
2. Add comparison UI (modal + drawer flow).
3. Improve AI explanations and confidence calibration.
4. Deploy staging stack (docker-compose + env wiring).
5. Add ML scoring baseline.

## Investor Demo UI Upgrade Plan

### Dashboard Hierarchy

1. Header.
2. KPI row.
3. AI recommendation hero panel.
4. Spend input.
5. Comparison.
6. Insights.
7. Charts.
8. Opportunity engine.

### New Components

1. `ComparisonModal.jsx`
2. `SavingsChart.jsx`
3. `SpendSlider.jsx`
4. `PersonaSelector.jsx`
5. `CardDetailDrawer.jsx`

### UX Additions

1. Onboarding screen.
2. Card comparison modal.
3. Reward simulation slider.
4. Yearly savings graph.
5. Persona selector.

## Deployment Runbook (Local)

1. `docker-compose up --build`
2. Open API docs at `http://localhost:8000/docs`
3. Verify database and cache service health.

## Deployment Targets (Cloud)

### Easiest

1. Railway.
2. Render.

### Scalable

1. AWS ECS.
2. GCP Cloud Run.

## Required Environment Variables

1. `DATABASE_URL`
2. `REDIS_URL`
3. `API_KEY`
4. `ENV=production`
