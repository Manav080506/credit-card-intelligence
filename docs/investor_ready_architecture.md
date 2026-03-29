# Investor-Ready Architecture

```text
react frontend
  -> api gateway (nestjs)
    -> ai intelligence layer (fastapi)
      -> feature engineering
      -> reward normalization
      -> recommendation engine
      -> postgres
      -> redis cache
      -> worker pipeline
        -> card dataset updates
```

## Why this scales

- Gateway isolates frontend from backend model evolution.
- FastAPI services can be split by domain as load grows.
- Redis serves low-latency recommendations for repeated spend shapes.
- Worker pipeline enables weekly/daily card updates without blocking API traffic.
- Postgres provides durable recommendation logs for product analytics and ML training.
