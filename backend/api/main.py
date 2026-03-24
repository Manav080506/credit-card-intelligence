from fastapi import FastAPI

from backend.api.routes.earn import router as earn_router
from backend.api.routes.redeem import router as redeem_router
from backend.api.routes.recommend import router as recommend_router
from backend.api.routes.cards import router as cards_router
from backend.api.routes.optimizer import router as optimizer_router
from backend.api.routes.compare import router as compare_router
from backend.api.routes.compare_optimizer import router as compare_optimizer_router
from backend.api.routes.combo_optimizer import router as combo_optimizer_router
from backend.api.routes.gap_recommend import router as gap_recommend_router

app = FastAPI(
    title="Credit Card Intelligence API",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(earn_router)
app.include_router(redeem_router)
app.include_router(recommend_router)
app.include_router(cards_router)

app.include_router(optimizer_router)

app.include_router(compare_router)
app.include_router(compare_optimizer_router)
app.include_router(combo_optimizer_router)
app.include_router(gap_recommend_router)
