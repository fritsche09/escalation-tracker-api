from pydantic import BaseModel, Field
from datetime import datetime

class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="open", min_length=1, max_length=50)
    priority: str = Field(default="low", min_length=1, max_length=50)
    
class TicketUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    status: str | None = None
    priority: str | None = None

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True