from fastapi import APIRouter, HTTPException, status, Body
from app.schemas.user import UserSchema
from app.services.user_service import create_user, get_user_by_email
from app.services.auth_service import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserSchema):
    try:
        new_user = create_user(user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
def login_user(payload: dict = Body(...)):
    email = payload.get("email")
    password = payload.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
        
    user = get_user_by_email(email)
    
    if not user or not verify_password(password, user.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(
        data={"sub": str(user["id"]), "role": user["role"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
