from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="open", min_length=1, max_length=50)
    priority: str = Field(default="low", min_length=1, max_length=50)

class TicketCreate(TicketBase):
    pass
    
class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True