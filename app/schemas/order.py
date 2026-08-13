from pydantic import BaseModel
from typing import Optional

class OrderSchema(BaseModel):
    item_id: int
    user_id: Optional[int] = None
    quantity: int
    price: float
    total_amount: float
    status: Optional[str] = None
    special_instructions: Optional[str] = None
