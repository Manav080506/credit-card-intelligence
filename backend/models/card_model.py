from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RewardConversion(BaseModel):
    type: str = 'cashback'
    value_per_point: float = 1.0


class CardModel(BaseModel):
    id: str
    name: str
    issuer: Optional[str] = None
    network: Optional[str] = None
    annual_fee: int = 0
    joining_fee: int = 0
    reward_type: Optional[str] = None
    online_shopping: float = 0
    dining: float = 0
    travel: float = 0
    utilities: float = 0
    reward_model: Dict[str, float] = Field(default_factory=dict)
    reward_conversion: RewardConversion = Field(default_factory=RewardConversion)
    caps: Dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
