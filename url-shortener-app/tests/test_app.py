from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_redirect():
    client = TestClient(create_app(), follow_redirects=False)
    assert client.get("/").status_code == 200
    created = client.post("/shorten", json={"url": "https://example.com/docs"}).json()
    response = client.get("/" + created["code"])
    assert response.status_code == 307
