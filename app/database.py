import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Global database variables
client = None
database = None
food_items_collection = None
counters_collection = None
users_collection = None

def connect_db():
    global client, database, food_items_collection, counters_collection, users_collection
    print("Connecting to MongoDB...")
    
    # Get URL from .env
    mongo_url = os.getenv("MONGO_URL")
    
    # If not found in .env, load local database
    if not mongo_url:
        mongo_url = "mongodb://localhost:27017"
    
    client = MongoClient(mongo_url)
    database = client["Restaurant_Application"]
    food_items_collection = database["food_items"]
    counters_collection = database["counters"]
    users_collection = database["users"]
    
    print("Successfully connected to MongoDB!")

def close_db():
    global client
    if client:
        print("Closing MongoDB connection...")
        client.close()
        print("MongoDB connection closed.")
