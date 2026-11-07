from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_auth():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    assert client.post("/register", json={"username": "aisha", "password": "secret1"}).status_code == 201
    token = client.post("/login", json={"username": "aisha", "password": "secret1"}).json()["access_token"]
    assert client.get("/me", headers={"Authorization": f"Bearer {token}"}).json()["username"] == "aisha"
