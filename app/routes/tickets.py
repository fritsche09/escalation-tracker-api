from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.models.ticket import Ticket
from app.models.user import User
from app.routes.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_ticket = Ticket(**ticket.model_dump(), user_id=user.id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("", response_model=list[TicketResponse])
def read_tickets(
    status: Optional[str] = None, 
    priority: Optional[str] = None, 
    limit: int = Query(5, ge=1, le=100), 
    offset: int = Query(0, ge=0), 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
    ):
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status.lower())
    if priority:
        query = query.filter(Ticket.priority == priority.lower())

    query = query.offset(offset).limit(limit)

    tickets = query.all()
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    current_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not current_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = ticket.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(current_ticket, key, value)

    db.commit()
    db.refresh(current_ticket)
    return current_ticket

@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()
    return None
