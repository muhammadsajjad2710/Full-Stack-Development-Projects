from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_toggle():
    client = TestClient(create_app())
    assert "text/html" in client.get("/").headers["content-type"]
    task = client.post("/tasks", json={"title": "Write tests"}).json()
    assert client.post(f"/tasks/{task['id']}/toggle").json()["done"] is True
