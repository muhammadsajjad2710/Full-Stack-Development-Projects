from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

def create_app() -> FastAPI:
    app = FastAPI(title="Chat App")
    app.state.rooms = {}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/rooms/{room}/history")
    def history(room: str):
        return {"room": room, "messages": app.state.rooms.get(room, [])}

    @app.websocket("/ws/{room}")
    async def chat(websocket: WebSocket, room: str):
        await websocket.accept()
        app.state.rooms.setdefault(room, [])
        try:
            while True:
                text = await websocket.receive_text()
                app.state.rooms[room].append(text)
                await websocket.send_json({"room": room, "message": text, "count": len(app.state.rooms[room])})
        except WebSocketDisconnect:
            return

    add_frontend(app)
    return app

app = create_app()
