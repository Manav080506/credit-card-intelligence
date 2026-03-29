from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.earn import router as earn_router
from backend.api.routes.redeem import router as redeem_router
from backend.api.routes.recommend import router as recommend_router
from backend.api.routes.cards import router as cards_router
from backend.api.routes.optimizer import router as optimizer_router
from backend.api.routes.compare_optimizer import router as compare_optimizer_router
from backend.api.routes.combo_optimizer import router as combo_optimizer_router
from backend.api.routes.gap_recommend import router as gap_recommend_router
from backend.api.routes.persona_optimizer import router as persona_optimizer_router
from backend.api.routes.transaction_optimizer import router as txn_optimizer_router
from backend.api.routes.wallet_advisor import router as wallet_advisor_router
from backend.api.routes.combo_optimizer_v2 import router as combo_optimizer_v2_router
from backend.api.routes.statement_analyzer import router as statement_router
from backend.api.routes.spend_simulator import router as simulator_router
from backend.api.routes.full_analysis import router as full_router
from backend.api.routes.merchant_classifier import router as merchant_router
from backend.api.routes.insight_v2 import router as insight_v2_router
from backend.api.routes.optimize import router as optimize_v2_router
from backend.api.routes.insights import router as insights_v2_router

app = FastAPI(
    title="Credit Card Intelligence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(earn_router)
app.include_router(redeem_router)
app.include_router(recommend_router)
app.include_router(cards_router)

app.include_router(optimizer_router)

app.include_router(compare_optimizer_router)
app.include_router(combo_optimizer_router)
app.include_router(gap_recommend_router)
app.include_router(persona_optimizer_router)
app.include_router(txn_optimizer_router)
app.include_router(wallet_advisor_router)
app.include_router(combo_optimizer_v2_router)
app.include_router(statement_router)
app.include_router(simulator_router)
app.include_router(full_router)
app.include_router(merchant_router)
app.include_router(insight_v2_router)
app.include_router(optimize_v2_router)
app.include_router(insights_v2_router)
