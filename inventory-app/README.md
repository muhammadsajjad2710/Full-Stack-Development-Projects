# Inventory App

Track stock and record sales from the UI.

FastAPI backend plus a browser UI. Do not expose it publicly as-is.

## Run

```powershell
cd D:\AI-Agents\Full-Stack-Development-Projects\inventory-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

```powershell
python -m pytest -q
```
