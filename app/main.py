from fastapi import FastAPI
from app.models.ticket import Ticket
from app.models.user import User
from app.database import Base, engine
from app.routes.tickets import router as tickets_router
from app.routes.auth import router as auth_router

app = FastAPI(title="Escalation Tracker API")
Base.metadata.create_all(bind=engine)
app.include_router(tickets_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Escalation Tracker API is running"}