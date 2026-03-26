from fastapi import FastAPI

app = FastAPI(title="Escalation Tracker API")


@app.get("/")
def root():
    return {"message": "Escalation Tracker API is running"}