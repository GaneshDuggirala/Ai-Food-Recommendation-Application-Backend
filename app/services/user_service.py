import app.database as db
from pymongo import ReturnDocument
from app.services.auth_service import get_password_hash

def get_next_user_id():
    counter_data = db.counters_collection.find_one_and_update(
        {"_id": "users"},  
        {"$inc": {"current_number": 1}},       
        return_document=ReturnDocument.AFTER,  
        upsert=True                            
    )
    return counter_data["current_number"]

def get_user_by_email(email: str):
    return db.users_collection.find_one({"email": email.lower()})

def create_user(user_data):
    new_user_dict = user_data.model_dump()
    
    if get_user_by_email(new_user_dict["email"]):
        raise ValueError("Email already registered")
        
    hashed_password = get_password_hash(new_user_dict["password"])
    new_user_dict["hashed_password"] = hashed_password
    del new_user_dict["password"]
    
    new_user_dict["email"] = new_user_dict["email"].lower()
    
    new_user_dict["role"] = "user"
    new_user_dict["id"] = get_next_user_id()
    
    db.users_collection.insert_one(new_user_dict)
    
    new_user_dict.pop("_id", None)
    new_user_dict.pop("hashed_password", None)
    
    return new_user_dict
