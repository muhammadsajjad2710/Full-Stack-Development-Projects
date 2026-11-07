from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_and_chat():
    app = create_app()
    client = TestClient(app)
    assert client.get("/").status_code == 200
    with client.websocket_connect("/ws/lobby") as ws:
        ws.send_text("hello")
        assert ws.receive_json()["message"] == "hello"
    assert client.get("/rooms/lobby/history").json()["messages"] == ["hello"]
