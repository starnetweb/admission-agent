from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Scholarship Agent - Test Mode", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing
subscribers = []
news_records = []
message_logs = []

@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "test"}

@app.post("/api/subscribers/")
async def create_subscriber(name: str, phone: str):
    subscriber = {
        "id": len(subscribers) + 1,
        "name": name,
        "phone": phone,
        "is_active": True
    }
    subscribers.append(subscriber)
    logger.info(f"Subscriber created: {name} ({phone})")
    return subscriber

@app.get("/api/subscribers/")
async def list_subscribers():
    return {"subscribers": subscribers, "total": len(subscribers)}

@app.get("/api/subscribers/{subscriber_id}")
async def get_subscriber(subscriber_id: int):
    for sub in subscribers:
        if sub["id"] == subscriber_id:
            return sub
    return {"error": "Subscriber not found"}

@app.post("/api/webhooks/facebook")
async def facebook_webhook(name: str, phone: str):
    subscriber = {
        "id": len(subscribers) + 1,
        "name": name,
        "phone": phone,
        "is_active": True
    }
    subscribers.append(subscriber)
    logger.info(f"Facebook lead captured: {name} ({phone})")
    return {"status": "created", "id": subscriber["id"]}

@app.get("/api/admin/stats")
async def get_statistics():
    return {
        "total_subscribers": len(subscribers),
        "active_subscribers": len([s for s in subscribers if s["is_active"]]),
        "total_news_articles": len(news_records),
        "total_messages_sent": len(message_logs),
        "successfully_sent": len([m for m in message_logs if m.get("status") == "sent"]),
        "failed_messages": len([m for m in message_logs if m.get("status") == "failed"])
    }

@app.post("/api/admin/run-agent")
async def manually_run_agent():
    logger.info("News agent triggered manually (test mode)")
    return {"status": "running", "message": "In test mode - news search disabled"}

@app.get("/api/admin/news/recent")
async def get_recent_news(limit: int = 10):
    return {"news": news_records[:limit]}

@app.get("/api/admin/messages/recent")
async def get_recent_messages(limit: int = 20):
    return {"messages": message_logs[:limit]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
