from fastapi.testclient import TestClient


def test_get_all_tickets(client):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_a_ticket(client):
    title = "GDXX(AMR R113)"
    description = "Broken heated display removal fixture"
    status = "open"

    json_file = {
        "title": title,
        "description": description,
        "status": status
    }

    create_response = client.post("/tickets", json=json_file)

    json_response = create_response.json()

    assert create_response.status_code == 201
    assert isinstance(json_response, dict)
    assert isinstance(json_response["id"], int)
    assert json_response["title"] == title
    assert json_response["description"] == description
    assert json_response["status"] == status

def test_get_ticket_by_id(client):
    title = "GDXX(AMR RXXX)"
    description = "Broken heated display removal fixture"
    status = "open"

    json_file = {
        "title": title,
        "description": description,
        "status": status
    }

    post_job = client.post("/tickets", json=json_file)
    json_response = post_job.json()
    ticket_id = json_response["id"]

    retrieve_job_by_id = client.get(f"/tickets/{ticket_id}")
    retrieved_job_json = retrieve_job_by_id.json()

    received = retrieved_job_json.keys()
    expected = {"title", "description", "status", "priority", "id", "created_at", "updated_at"}

    assert retrieve_job_by_id.status_code == 200
    assert isinstance(retrieved_job_json["id"], int)
    assert received == expected
    assert retrieved_job_json["title"] == title
    assert retrieved_job_json["description"] == description

def test_get_ticket_not_found(client):
    non_existent_id = 99999
    expected_code = 404
    expected_key = "detail"
    expected_value = "Ticket not found"

    retrieve_job_by_id = client.get(f"/tickets/{non_existent_id}")

    assert retrieve_job_by_id.status_code == expected_code
    assert retrieve_job_by_id.json()[expected_key] == expected_value

def test_update_ticket(client):
    title = "GDXX(AMR RXXX)"
    description = "Broken heated display removal fixture"
    status = "open"

    json_file = {
        "title": title,
        "description": description,
        "status": status
    }

    original_ticket = client.post("/tickets", json=json_file)
    original_ticket_json = original_ticket.json()
    ticket_id = original_ticket_json["id"]

    title = "Updated data (EMEIA RXXX)"
    description = "Broken Display Press"
    status = "open"
    priority = "high"

    json_file = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority
    }

    
    updated_ticket = client.patch(f"/tickets/{ticket_id}", json=json_file)
    updated_ticket_json = updated_ticket.json()

    assert updated_ticket.status_code == 200
    assert updated_ticket_json["id"] == ticket_id
    assert updated_ticket_json["title"] == title
    assert updated_ticket_json["description"] == description
    assert updated_ticket_json["status"] == status
    assert updated_ticket_json["priority"] == priority


def test_partial_update_ticket(client):
    title = "GDXX(AMR RXXX)"
    description = "Broken heated display removal fixture"
    status = "open"


    json_file = {
        "title": title,
        "description": description,
        "status": status,
    }

    original_ticket = client.post("/tickets", json=json_file)
    original_ticket_json = original_ticket.json()
    ticket_id = original_ticket_json["id"]

    title = "Updated data (EMEIA RXXX)"

    json_file = {
        "title": title
    }
    
    updated_ticket = client.patch(f"/tickets/{ticket_id}", json=json_file)
    updated_ticket_json = updated_ticket.json()

    assert updated_ticket.status_code == 200
    assert updated_ticket_json["id"] == ticket_id
    assert updated_ticket_json["title"] == title
    assert updated_ticket_json["description"] == description
    assert updated_ticket_json["status"] == status
    assert updated_ticket_json["priority"] == original_ticket_json["priority"]


def test_delete_ticket(client):
    title = "GDXX(AMR RXXX)"
    description = "Broken heated display removal fixture"
    status = "open"

    json_file = {
        "title": title,
        "description": description,
        "status": status
    }

    original_ticket = client.post("/tickets", json=json_file)
    original_ticket_json = original_ticket.json()
    ticket_id = original_ticket_json["id"]

    delete_ticket = client.delete(f"/tickets/{ticket_id}")

    assert delete_ticket.status_code == 204

    verify_deleted = client.get(f"/tickets/{ticket_id}")
    assert verify_deleted.status_code == 404

            
def test_delete_ticket_not_found(client):
    non_existent_id = 99999
    expected_code = 404
    expected_key = "detail"
    expected_value = "Ticket not found"

    retrieve_job_by_id = client.delete(f"/tickets/{non_existent_id}")

    assert retrieve_job_by_id.status_code == expected_code
    assert retrieve_job_by_id.json()[expected_key] == expected_value
    

