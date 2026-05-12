import logging
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import Subscriber, NewsRecord, MessageLog
from src.newsapi import search_scholarship_news, format_article_for_whatsapp
from src.whatsapp import send_whatsapp_message

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        cron_schedule = "0 8 * * *"
        scheduler.add_job(
            run_news_agent,
            CronTrigger.from_crontab(cron_schedule),
            id="scholarship_agent",
            name="Scholarship News Agent",
            replace_existing=True
        )
        scheduler.start()
        logger.info(f"Scheduler started with cron: {cron_schedule}")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")

def run_news_agent():
    logger.info("Starting news agent...")
    try:
        asyncio.run(fetch_and_distribute_news())
    except Exception as e:
        logger.error(f"Error in news agent: {e}")

async def fetch_and_distribute_news():
    db = SessionLocal()

    try:
        logger.info("Fetching scholarship news...")
        articles = await search_scholarship_news()

        if not articles:
            logger.warning("No articles found")
            return

        logger.info(f"Found {len(articles)} articles")

        for article in articles:
            url = article.get("url", "")
            existing = db.query(NewsRecord).filter(NewsRecord.url == url).first()

            if not existing:
                news = NewsRecord(
                    title=article.get("title", "")[:500],
                    description=article.get("description", ""),
                    url=url,
                    source=article.get("source", {}).get("name"),
                    category="scholarship",
                    published_at=article.get("publishedAt")
                )
                db.add(news)
                db.commit()
                db.refresh(news)
                logger.info(f"Saved news: {news.title[:50]}")

                await distribute_news_to_subscribers(db, news, article)

    finally:
        db.close()

async def distribute_news_to_subscribers(db: Session, news: NewsRecord, article: dict):
    """Send news to all active subscribers"""

    subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()

    if not subscribers:
        logger.warning("No active subscribers found")
        return

    logger.info(f"Distributing news to {len(subscribers)} subscribers")

    message_text = format_article_for_whatsapp(article)

    for subscriber in subscribers:
        try:
            message_id = await send_whatsapp_message(
                subscriber.phone,
                message_text
            )

            log_entry = MessageLog(
                subscriber_id=subscriber.id,
                news_id=news.id,
                status="sent" if message_id else "failed",
                message_id=message_id
            )
            db.add(log_entry)
            db.commit()

        except Exception as e:
            logger.error(f"Error sending to {subscriber.phone}: {e}")
            log_entry = MessageLog(
                subscriber_id=subscriber.id,
                news_id=news.id,
                status="failed",
                error_message=str(e)
            )
            db.add(log_entry)
            db.commit()

        await asyncio.sleep(0.5)
