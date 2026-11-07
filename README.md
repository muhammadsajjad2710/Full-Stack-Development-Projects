# Full Stack Development Projects

Ten local **full-stack** apps. Each one has a FastAPI backend and an HTML/CSS/JavaScript UI in the same project. No paid APIs.

These apps have no production authentication story unless noted. Do not expose them publicly as-is.

## Projects

| # | Project | What you get |
| --- | --- | --- |
| 1 | [todo-app](todo-app/) | Todo list with toggle |
| 2 | [notes-app](notes-app/) | Notes with create and delete |
| 3 | [blog-app](blog-app/) | Blog posts and comments |
| 4 | [auth-dashboard](auth-dashboard/) | Register, login, and profile |
| 5 | [bookstore-app](bookstore-app/) | Book catalog with search |
| 6 | [inventory-app](inventory-app/) | Products and sales |
| 7 | [url-shortener-app](url-shortener-app/) | Short links with a UI |
| 8 | [issue-tracker-app](issue-tracker-app/) | Open and close issues |
| 9 | [chat-app](chat-app/) | WebSocket chat |
| 10 | [recipe-book-app](recipe-book-app/) | Recipes with ingredients and steps |

## Quick start

```powershell
cd D:\AI-Agents\Full-Stack-Development-Projects\todo-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000
