# Microservices Architecture

```text
frontend (react)
  -> api gateway (nestjs)
    -> optimization service (fastapi)
      -> dataset service
      -> postgres
      -> redis cache
```

## Processing Flow

1. User provides spend profile in frontend.
2. Frontend calls gateway optimize endpoint.
3. Gateway forwards to fastapi optimization service.
4. Optimizer computes card ranking from optimizer dataset layer.
5. Metadata layer enriches card output for explainable UI.
6. Insights are generated and returned to frontend.
7. Frontend updates charts, recommendation cards, and motion states.
