from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.models.ticket import Ticket
from app.database import get_db

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(**ticket.model_dump())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("", response_model=list[TicketResponse])
def read_tickets(db: Session = Depends(get_db)):
    all_tickets = db.query(Ticket).all()
    return all_tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
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
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()
    return None
