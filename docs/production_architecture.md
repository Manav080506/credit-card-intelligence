# Production Architecture

## Directory Layout

```text
frontend/
  pages/
  components/
  hooks/
  core/api/
  state/
  theme/

backend/
  api/
  engine/
  schemas/
  workers/
  data/

gateway/
  nestjs API gateway

infra/
  nginx
  docker
  postgres
  redis
  aws
```

## Final System Flow

1. User spend input
2. React hook normalizes category payload
3. API gateway forwards request
4. FastAPI optimizer computes best card from dataset
5. Insight payload returned to frontend
6. UI state updates and motion transitions trigger
