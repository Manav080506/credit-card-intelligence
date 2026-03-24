from fastapi import APIRouter

from backend.engine.persona_loader import load_persona

from backend.engine.wallet_optimizer import optimize_wallet


router = APIRouter(
 prefix="/optimize_persona",
 tags=["Persona"]
)


@router.post("")
def optimize_persona_wallet(payload:dict):

 persona = load_persona(
  payload["persona_id"]
 )

 return optimize_wallet(

  card_ids=payload["card_ids"],

  monthly_spend=persona["monthly_spend"]

 )
