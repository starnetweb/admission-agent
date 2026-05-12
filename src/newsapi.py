import os
import httpx
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
NEWSAPI_BASE_URL = "https://newsapi.org/v2"

async def search_scholarship_news() -> List[Dict]:
    if not NEWSAPI_KEY:
        logger.warning("NEWSAPI_KEY not configured")
        return []

    queries = [
        "Nigeria scholarships 2024 2025",
        "Nigerian university admissions",
        "scholarship opportunities Nigeria",
        "Nigerian students visa sponsorship"
    ]

    all_articles = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        for query in queries:
            try:
                response = await client.get(
                    f"{NEWSAPI_BASE_URL}/everything",
                    params={
                        "q": query,
                        "sortBy": "publishedAt",
                        "language": "en",
                        "apiKey": NEWSAPI_KEY,
                        "pageSize": 10
                    }
                )
                response.raise_for_status()
                data = response.json()

                if data.get("articles"):
                    all_articles.extend(data["articles"])
                    logger.info(f"Found {len(data['articles'])} articles for '{query}'")

            except httpx.RequestError as e:
                logger.error(f"Request error for query '{query}': {e}")
            except Exception as e:
                logger.error(f"Error searching for '{query}': {e}")

    return deduplicate_articles(all_articles)

def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    seen_urls = set()
    unique = []

    for article in articles:
        url = article.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(article)

    return unique

def format_article_for_whatsapp(article: Dict) -> str:
    title = article.get("title", "No title")
    description = article.get("description", "")
    url = article.get("url", "")
    source = article.get("source", {}).get("name", "Unknown")

    message = f"""
📰 *{title}*

_{description[:200]}..._

Source: {source}
Read more: {url}
"""
    return message.strip()
