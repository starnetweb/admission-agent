import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Subscriber
from src.schemas import SubscriberCreate, SubscriberUpdate, SubscriberResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=SubscriberResponse)
async def create_subscriber(
    subscriber_data: SubscriberCreate,
    db: Session = Depends(get_db)
):
    """Create a new subscriber"""

    phone = subscriber_data.phone.strip()
    existing = db.query(Subscriber).filter(
        Subscriber.phone == phone
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    subscriber = Subscriber(
        name=subscriber_data.name.strip(),
        phone=phone,
        is_active=True
    )
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)

    logger.info(f"Subscriber created: {subscriber.name}")
    return subscriber

@router.get("/", response_model=List[SubscriberResponse])
async def list_subscribers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all subscribers"""

    subscribers = db.query(Subscriber).offset(skip).limit(limit).all()
    return subscribers

@router.get("/{subscriber_id}", response_model=SubscriberResponse)
async def get_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific subscriber"""

    subscriber = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    return subscriber

@router.put("/{subscriber_id}", response_model=SubscriberResponse)
async def update_subscriber(
    subscriber_id: int,
    subscriber_data: SubscriberUpdate,
    db: Session = Depends(get_db)
):
    """Update a subscriber"""

    subscriber = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    if subscriber_data.name is not None:
        subscriber.name = subscriber_data.name
    if subscriber_data.is_active is not None:
        subscriber.is_active = subscriber_data.is_active

    db.commit()
    db.refresh(subscriber)

    logger.info(f"Subscriber updated: {subscriber.id}")
    return subscriber

@router.delete("/{subscriber_id}")
async def delete_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db)
):
    """Delete a subscriber (soft delete)"""

    subscriber = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    subscriber.is_active = False
    db.commit()

    logger.info(f"Subscriber deactivated: {subscriber.id}")
    return {"status": "deleted"}
