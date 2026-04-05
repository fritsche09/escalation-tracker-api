# Escalation Tracker API

A backend service built with FastAPI for managing and tracking support tickets. The API supports full CRUD operations, filtering, pagination, and partial updates.

## Features:
- Full CRUD operations for tickets
- Partial updates using PATCH
- Filtering by status and priority 
- Pagination using limits and offsets
- Input validation with Pydantic

## Tech Stack:
- Python
- FastAPI 
- Pydantic
- PostgreSQL
- SQLAlchemy

## Project Structure
```
app/
├── core/
├── models/
├── routes/
├── schemas/
├── database.py
└── main.py
```

## How to run locally

1. Clone the repository 
```
git clone https://github.com/fritsche09/escalation-tracker-api.git
cd escalation-tracker-api
```
2. Create and activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```
3. Installation
```
pip3 install -r requirements.txt
```
4. Create a `.env` file based on `.env.example`
5. Setup a PostgreSQL database and update your `.env` file:
- Create a new PostgreSQL database
- Update your credentials:
`DATABASE_URL=postgresql://username:password@localhost/escalation_tracker`
6. Start the server
`uvicorn app.main:app --reload`

## API Endpoints

| Method | Endpoint         | Description                  |
|--------|------------------|------------------------------|
| POST   | /tickets         | Create a new ticket          |
| GET    | /tickets         | Get all tickets              |
| GET    | /tickets/{id}    | Get a ticket by ID           |
| PATCH  | /tickets/{id}    | Update a ticket              |
| DELETE | /tickets/{id}    | Delete a ticket              |

### Query parameters:

|Endpoint      | Query parameters               | Example           | Description                          | 
|--------------|--------------------------------|-------------------|--------------------------------------|
|/tickets      | /limit/                        |  ?limit=`10`      | Limits response to `10` tickets.     | 
|              | /offset/                       |  ?offset=`1`      |  Skips result by `1`                 | 
|              | /status/                       |  ?status=`open`   | Returns results with `open` status   |
|              | /priority/                     |  ?priority=`high` | Returns results with `high` priority |


### Example request

POST /tickets: 

```json
{
  "title": "Printer Issue",
  "description": "Paper jam",
  "priority": "high"
}
```

Response body: 
```json
{
  "title": "Printer Issue",
  "description": "Paper jam",
  "status": "open",
  "priority": "high",
  "id": 1,
  "created_at": "2026-03-29T20:13:16.969111",
  "updated_at": "2026-03-29T20:13:16.969111"
}
```

## Running Tests

1. Create a test database in PostgreSQL called `escalation_tracker_test`
2. Run the test suite:
```bash
   pytest tests/ -v
```