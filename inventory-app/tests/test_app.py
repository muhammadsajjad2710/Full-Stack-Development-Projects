from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_sell():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    product = client.post("/products", json={"name": "Mug", "stock": 5, "price_cents": 499}).json()
    assert client.post(f"/products/{product['id']}/sell", json={"quantity": 2}).json()["remaining"] == 3
