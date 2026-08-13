import app.database as db
from pymongo import ReturnDocument
from datetime import datetime

def get_next_order_id():
    counter_data = db.counters_collection.find_one_and_update(
        {"_id": "orders"},  
        {"$inc": {"current_number": 1}},       
        return_document=ReturnDocument.AFTER,  
        upsert=True                            
    )
    return counter_data["current_number"]

def create_order(user_id: int, order_data):
    order_dict = order_data.model_dump()
    order_dict["order_id"] = f"ORD-{get_next_order_id()}"
    order_dict["user_id"] = user_id
    order_dict["status"] = "Placed"
    order_dict["created_at"] = datetime.utcnow()
    
    db.orders_collection.insert_one(order_dict)
    order_dict.pop("_id", None)
    return order_dict

def get_user_orders(user_id: int):
    orders = []
    for order in db.orders_collection.find({"user_id": user_id}).sort("created_at", -1):
        order.pop("_id", None)
        orders.append(order)
    return orders

def get_all_orders():
    orders = []
    for order in db.orders_collection.find().sort("created_at", -1):
        order.pop("_id", None)
        orders.append(order)
    return orders

def update_order_status(order_id: str, status: str):
    valid_statuses = ["Placed", "Confirmed", "Preparing", "Ready", "Picked Up"]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
    updated = db.orders_collection.find_one_and_update(
        {"order_id": order_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER
    )
    if updated:
        updated.pop("_id", None)
        return updated
    return None
