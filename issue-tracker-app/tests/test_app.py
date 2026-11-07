from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_close():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    issue = client.post("/issues", json={"title": "Login 500", "description": "crash"}).json()
    assert client.post(f"/issues/{issue['id']}/close").json()["open"] is False
