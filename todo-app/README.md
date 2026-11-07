# Todo App

Add tasks and mark them done. FastAPI backend plus a browser UI.

FastAPI backend plus a browser UI. Do not expose it publicly as-is.

## Run

```powershell
cd D:\AI-Agents\Full-Stack-Development-Projects\todo-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

```powershell
python -m pytest -q
```
