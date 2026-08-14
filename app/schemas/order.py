from pydantic import BaseModel
from typing import Optional, List

class OrderSchema(BaseModel):
    item_id: List[int]
    user_id: Optional[int] = None
    quantity: List[int]
    price: List[float]
    total_amount: float
    status: Optional[str] = None
    special_instructions: Optional[str] = None
