from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_notes():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    note = client.post("/notes", json={"title": "Milk", "body": "2L"}).json()
    assert client.delete(f"/notes/{note['id']}").status_code == 204
