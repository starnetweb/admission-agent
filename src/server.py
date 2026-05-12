from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
import os

from src.database import init_db
from src.agent import start_scheduler, stop_scheduler
from src.routes import webhooks, subscribers, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    init_db()
    start_scheduler()
    yield
    logger.info("Shutting down...")
    stop_scheduler()

app = FastAPI(title="Scholarship Agent", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(subscribers.router, prefix="/api/subscribers", tags=["subscribers"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def signup_form():
    signup_html_path = os.path.join(os.path.dirname(__file__), "signup.html")
    with open(signup_html_path, "r") as f:
        return f.read()

@app.get("/signup", response_class=HTMLResponse)
async def signup_page():
    signup_html_path = os.path.join(os.path.dirname(__file__), "signup.html")
    with open(signup_html_path, "r") as f:
        return f.read()

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "admin_dashboard.html")
    with open(dashboard_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
