from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    @field_validator("status", "priority", mode="before")
    @classmethod
    def lower_case(cls, value: Optional[str]): 
        if value is None:
            return value
        return value.lower()
    
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="open", min_length=1, max_length=50)
    priority: str = Field(default="low", min_length=1, max_length=50)


class TicketCreate(TicketBase):
    pass
    
class TicketUpdate(BaseModel):
    @field_validator("status", "priority", mode="before")
    @classmethod
    def lower_case(cls, value: Optional[str]): 
        if value is None:
            return value
        return value.lower()
    
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    priority: Optional[str] = Field(None, min_length=1, max_length=50)

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True