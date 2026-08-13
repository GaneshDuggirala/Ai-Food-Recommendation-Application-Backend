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

@router.get("/search", status_code=status.HTTP_200_OK)
def search_food_items(q: str):
    from app.services import ai_service
    
    print(f"\n==============================================")
    print(f"User\n │\n │ \"{q}\"\n ▼\nAI\n │")
    all_items = food_item_service.get_all_food_items()
    
    if not q or not q.strip():
        return all_items
        
    categories = list(set([item.get("category") for item in all_items if item.get("category")]))
    tags_lists = [item.get("dietary_tags", []) for item in all_items]
    tags = list(set([tag for sublist in tags_lists for tag in sublist]))
        
    filters = ai_service.extract_filters_with_ai(q, categories, tags)
    
    # Query database
    print(f" │\n ▼\nDatabase\n │")
    matched_items = food_item_service.search_items_by_filter(filters)
    
    if matched_items:
        print(f" ├── Matching items → returning {len(matched_items)} items")
    else:
        print(" └── No matching items → \"Not available\"")
    print(f"==============================================\n")
        
    return matched_items
