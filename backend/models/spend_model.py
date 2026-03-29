from pydantic import BaseModel


class SpendModel(BaseModel):
    online_shopping: float = 0
    dining: float = 0
    travel: float = 0
    groceries: float = 0
    fuel: float = 0
    utilities: float = 0
