from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
