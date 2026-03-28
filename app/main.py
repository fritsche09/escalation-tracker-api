from fastapi import FastAPI
from app.models.ticket import Ticket
from app.database import Base, engine
from app.routes.tickets import router

app = FastAPI(title="Escalation Tracker API")
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Escalation Tracker API is running"}