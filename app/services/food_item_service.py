import app.database as db
from pymongo import ReturnDocument



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
