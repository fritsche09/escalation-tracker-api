from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UserEmailBase(BaseModel):
    @field_validator("email", mode="before")
    @classmethod
    def lower_case(cls, value: str):
        if value is None:
            return value
        return value.lower()
    
    email: str = Field(..., min_length=1, max_length=100)

class UserRegister(UserEmailBase):
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(UserEmailBase):
    password: str = Field(..., min_length=8, max_length=100)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str 
    email: str
    is_active: bool
    created_at: datetime
        
    class Config:
        from_attributes = True