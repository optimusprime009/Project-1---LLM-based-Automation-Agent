from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_data_from_api():
    response = client.post("/run", json={"task": "fetch data from api"})
    assert response.status_code == 200
    assert "Fetched data from API and saved." in response.json()["message"]

def test_read_api_data():
    response = client.get("/read?path=data/api-data.json")
    assert response.status_code == 200
    assert response.json()["content"] is not None

def test_invalid_task():
    response = client.post("/run", json={"task": "invalid task"})
    assert response.status_code == 400
    assert "Unknown task" in response.json()["detail"]

def test_restricted_path():
    response = client.get("/read?path=secrets/passwords.txt")
    assert response.status_code == 400
    assert "Access to this path is restricted." in response.json()["detail"]