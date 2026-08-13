from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routes.status_routes import router as status_router
from app.routes.food_item_routes import router as food_item_router
from app.routes.auth_routes import router as auth_router
from app.routes.order_routes import router as order_router
from app.database import connect_db, close_db

load_dotenv()

app = FastAPI()

# 1. Read allowed frontend ports from .env, or use Vite's defaults
allowed_origins = os.getenv("FRONTEND_URL", "http://localhost:5173,http://127.0.0.1:5173").split(",")

# 2. Add CORS Middleware to explicitly allow our frontend React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, PUT, DELETE, PATCH
    allow_headers=["*"],
)

# To connect mongo Db on start up
@app.on_event("startup")
def startup_event():
    connect_db()
# To close mongo Db connection on shutdown
@app.on_event("shutdown")
def shutdown_event():
    close_db()

# Register routes
app.include_router(status_router, prefix="/api")
app.include_router(food_item_router, prefix="/api/items")
app.include_router(auth_router, prefix="/api")
app.include_router(order_router, prefix="/api/orders")
