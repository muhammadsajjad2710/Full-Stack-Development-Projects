from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_recipe():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    created = client.post("/recipes", json={"title": "Chai", "ingredients": "tea, milk", "steps": "boil"}).json()
    assert created["title"] == "Chai"
