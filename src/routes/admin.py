import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database import get_db
from src.models import Subscriber, NewsRecord, MessageLog
from src.agent import run_news_agent

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Get overall statistics"""

    total_subscribers = db.query(func.count(Subscriber.id)).scalar()
    active_subscribers = db.query(func.count(Subscriber.id)).filter(
        Subscriber.is_active == True
    ).scalar()
    total_news = db.query(func.count(NewsRecord.id)).scalar()
    total_messages = db.query(func.count(MessageLog.id)).scalar()
    sent_messages = db.query(func.count(MessageLog.id)).filter(
        MessageLog.status == "sent"
    ).scalar()

    return {
        "total_subscribers": total_subscribers,
        "active_subscribers": active_subscribers,
        "inactive_subscribers": total_subscribers - active_subscribers,
        "total_news_articles": total_news,
        "total_messages_sent": total_messages,
        "successfully_sent": sent_messages,
        "failed_messages": total_messages - sent_messages
    }

@router.post("/run-agent")
async def manually_run_agent():
    """Manually trigger the news agent"""

    try:
        run_news_agent()
        logger.info("News agent triggered manually")
        return {"status": "running", "message": "Agent started"}

    except Exception as e:
        logger.error(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/recent")
async def get_recent_news(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recently added news articles"""

    news = db.query(NewsRecord).order_by(
        NewsRecord.created_at.desc()
    ).limit(limit).all()

    return news

@router.get("/messages/recent")
async def get_recent_messages(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get recent message logs"""

    messages = db.query(MessageLog).order_by(
        MessageLog.created_at.desc()
    ).limit(limit).all()

    return messages

@router.get("/messages/failed")
async def get_failed_messages(db: Session = Depends(get_db)):
    """Get failed messages"""

    messages = db.query(MessageLog).filter(
        MessageLog.status == "failed"
    ).order_by(MessageLog.created_at.desc()).all()

    return messages
