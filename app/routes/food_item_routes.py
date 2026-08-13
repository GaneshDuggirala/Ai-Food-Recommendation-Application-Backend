from fastapi import APIRouter, status
from app.schemas.food_item import FoodItemCreate
from app.services import food_item_service

router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_new_food_item(item: FoodItemCreate):
    print("Received request to add food item:", item)
    return food_item_service.create_food_item(item)

@router.get("/get-all", status_code=status.HTTP_200_OK)
def get_all_food_items():
    return food_item_service.get_all_food_items()

@router.put("/update/{item_id}", status_code=status.HTTP_200_OK)
def update_food_item(item_id: int, item: FoodItemCreate):
    # The item_id comes from the URL, but the 'item' data comes entirely from the body
    return food_item_service.update_food_item(item_id, item)

@router.delete("/delete/{item_id}", status_code=status.HTTP_200_OK)
def delete_food_item(item_id: int):
    # Just need the ID from the URL to delete it!
    return food_item_service.delete_food_item(item_id)
