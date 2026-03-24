from fastapi import APIRouter
from backend.engine.merchant_classifier import classify_merchant


router = APIRouter(

    prefix="/classify_merchant",

    tags=["Merchant"]

)


@router.post("")

def classify(

    payload: dict

):

    return classify_merchant(

        payload["merchant"]

    )
