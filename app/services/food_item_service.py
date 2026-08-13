import app.database as db
from pymongo import ReturnDocument
import re


def get_next_id_number():
    counter_data = db.counters_collection.find_one_and_update(
        {"_id": "food_items"},  
        {"$inc": {"current_number": 1}},       
        return_document=ReturnDocument.AFTER,  
        upsert=True                            
    )
    return counter_data["current_number"]



def create_food_item(item_data):
    new_item_dict = item_data.model_dump()
    new_item_dict["id"] = get_next_id_number()
    db.food_items_collection.insert_one(new_item_dict)
    
    new_item_dict.pop("_id", None)
    return new_item_dict



def get_all_food_items():
    all_items_list = []
    
    for item in db.food_items_collection.find():
        # Add the clean item to our final list
        item.pop("_id", None)
        all_items_list.append(item)
        
    return all_items_list

def update_food_item(item_id, update_data):
    update_dict = update_data.model_dump()
    db.food_items_collection.update_one(
        {"id": item_id},        
        {"$set": update_dict}   
    )
    
    return {"message": f"Item {item_id} successfully updated!"}

def delete_food_item(item_id):
    db.food_items_collection.delete_one({"id": item_id})
    
    return {"message": f"Item {item_id} successfully deleted!"}


def search_items_by_filter(filters: dict):
    query = {}
    
    if filters.get("category"):
        query["category"] = {"$regex": filters["category"], "$options": "i"}
        
    if filters.get("dietary") and isinstance(filters["dietary"], list) and len(filters["dietary"]) > 0:
        query["dietary_tags"] = {"$in": [re.compile(tag, re.IGNORECASE) for tag in filters["dietary"]]}
        
    if filters.get("is_fried") is not None:
        query["is_fried"] = filters["is_fried"]
        
    if filters.get("max_price") is not None or filters.get("min_price") is not None:
        price_query = {}
        if filters.get("max_price") is not None:
            try:
                price_query["$lte"] = float(filters["max_price"])
            except (ValueError, TypeError):
                pass
        if filters.get("min_price") is not None:
            try:
                price_query["$gte"] = float(filters["min_price"])
            except (ValueError, TypeError):
                pass
                
        if price_query:
            query["price"] = price_query
    if filters.get("keywords") and isinstance(filters["keywords"], list) and len(filters["keywords"]) > 0:
        keyword_conditions = []
        for kw in filters["keywords"]:
            if isinstance(kw, str) and kw.strip():
                keyword_regex = re.compile(kw.strip(), re.IGNORECASE)
                keyword_conditions.append({"name": {"$regex": keyword_regex}})
                keyword_conditions.append({"description": {"$regex": keyword_regex}})
        
        if keyword_conditions:
            query["$or"] = keyword_conditions
            
    print(f"--- Executing MongoDB Query: {query} ---")
    
    all_items_list = []
    for item in db.food_items_collection.find(query):
        item.pop("_id", None)
        all_items_list.append(item)
        
    return all_items_list
