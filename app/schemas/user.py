from pydantic import BaseModel, EmailStr

from enum import Enum

class UserRole(str, Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserBase(BaseModel):
    name:str
    email:EmailStr
    password:str
    role: str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
        
class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str
    
    class Config:
        from_attributes=True
        