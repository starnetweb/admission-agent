import os
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Subscriber
from src.schemas import SubscriberCreate

logger = logging.getLogger(__name__)

router = APIRouter()

WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN", "your-secret-token")

@router.post("/facebook")
async def facebook_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Receive subscriber data from Facebook Lead Form"""

    try:
        data = await request.json()

        if not data.get("name") or not data.get("phone"):
            raise HTTPException(status_code=400, detail="Missing required fields")

        existing = db.query(Subscriber).filter(
            Subscriber.phone == data["phone"]
        ).first()

        if existing:
            logger.info(f"Subscriber already exists: {data['phone']}")
            return {"status": "already_exists", "id": existing.id}

        subscriber = Subscriber(
            name=data["name"],
            phone=data["phone"],
            is_active=True
        )
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)

        logger.info(f"New subscriber created: {subscriber.name} ({subscriber.phone})")
        return {"status": "created", "id": subscriber.id}

    except Exception as e:
        logger.error(f"Error processing Facebook webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/verify")
async def verify_webhook(token: str):
    """Verify webhook token (optional, for testing)"""

    if token != WEBHOOK_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    return {"status": "verified"}
