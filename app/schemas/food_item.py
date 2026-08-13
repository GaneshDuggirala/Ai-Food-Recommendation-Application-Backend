from pydantic import BaseModel
from typing import List, Optional

class FoodItemCreate(BaseModel):
    name: str
    description: str
    category: str
    price: float
    dietary_tags: List[str] = []
    is_fried: bool = False
    availability: bool = True
    image_url: Optional[str] = None
