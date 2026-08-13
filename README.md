# Restaurant Application - Backend

## Tech Stack
- Framework: FastAPI (Python)
- Database: MongoDB (using PyMongo)
- Data Validation: Pydantic
- Security: Passlib for passwords, python-jose for JWT login
- AI Search: Groq API to understand user search queries

## Architecture Decisions
- AI Search Logic: Instead of using complex AI vector databases, we use the Groq AI to read what the user types (like "spicy food") and turn it into a simple JSON filter. The backend uses this JSON to search MongoDB quickly and accurately.
- Flat Order Data: Orders are saved as simple, flat records in the database rather than deeply nested items. This makes it easier to update order statuses.

## Setup Instructions

### Prerequisites
- Python (3.10 or newer)
- MongoDB (running locally on port 27017)

### Getting Started
1. Open your terminal and go to the backend folder:
   `cd backend`

2. Create a virtual environment:
   `python -m venv venv`

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate`

4. Install the required packages:
   `pip install -r requirements.txt`

5. Create a `.env` file and add these variables:
   ```
   MONGO_URL=mongodb://localhost:27017
   JWT_SECRET_KEY=your_secret_key_here
   GROQ_API_KEY=your_groq_api_key_here
   FRONTEND_URL=http://localhost:5173,http://127.0.0.1:5173
   ```

6. Run the backend server:
   `uvicorn app.main:app --reload`
   (The backend will be available at http://127.0.0.1:8000)

## Assumptions Made
- Single Item Orders: The app assumes each item in the cart is saved as its own order record. If a user buys 3 different items, it creates 3 separate orders.
- Local Database: MongoDB is expected to run locally on your machine without a password for development testing.
- Admin Users: The "admin" role is given to a user directly in the database.