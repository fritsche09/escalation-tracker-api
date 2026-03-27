from fastapi import FastAPI
from app.models.ticket import Ticket
from app.database import Base, engine

app = FastAPI(title="Escalation Tracker API")
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Escalation Tracker API is running"}