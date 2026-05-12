from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class SubscriberCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    interests: Optional[str] = None
    institutions: Optional[str] = None

class SubscriberUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class SubscriberResponse(BaseModel):
    id: int
    name: str
    phone: str
    interests: Optional[str]
    institutions: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class NewsCreate(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: Optional[str] = None
    category: str = "scholarship"
    published_at: Optional[datetime] = None

class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    url: str
    source: Optional[str]
    category: str
    published_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class MessageLogResponse(BaseModel):
    id: int
    subscriber_id: int
    news_id: int
    status: str
    message_id: Optional[str]
    error_message: Optional[str]
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class FacebookWebhookData(BaseModel):
    name: str
    phone: str
