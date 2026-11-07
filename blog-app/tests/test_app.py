from fastapi.testclient import TestClient
from app.main import create_app

def test_ui_post_comment():
    client = TestClient(create_app())
    assert client.get("/").status_code == 200
    post = client.post("/posts", json={"title": "Hello", "body": "World"}).json()
    comment = client.post(f"/posts/{post['id']}/comments", json={"author": "Aisha", "body": "Nice"})
    assert comment.status_code == 201
