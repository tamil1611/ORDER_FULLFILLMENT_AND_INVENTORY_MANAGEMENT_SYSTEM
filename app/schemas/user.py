from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role:str
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
    
class ChangePassword(BaseModel):
    old_password:str
    new_password:str