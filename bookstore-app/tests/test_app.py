from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_search():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965})
    assert client.get("/books", params={"q": "dune"}).json()["total"] == 1
