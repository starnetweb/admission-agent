import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_API_URL = "https://graph.instagram.com/v18.0"

async def send_whatsapp_message(
    recipient_phone: str,
    message_text: str
) -> Optional[str]:
    """Send a WhatsApp message using Meta API"""

    if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_ID:
        logger.error("WhatsApp credentials not configured")
        return None

    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": format_phone_number(recipient_phone),
        "type": "text",
        "text": {"body": message_text}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            message_id = data.get("messages", [{}])[0].get("id")
            logger.info(f"Message sent to {recipient_phone}: {message_id}")
            return message_id

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error sending to {recipient_phone}: {e.response.text}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request error sending to {recipient_phone}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error sending to {recipient_phone}: {e}")
        return None

def format_phone_number(phone: str) -> str:
    """Format phone number to E.164 format"""
    phone = phone.replace("+", "").replace(" ", "").replace("-", "")

    if not phone.startswith("234") and len(phone) == 10:
        phone = "234" + phone[1:]

    if not phone.startswith("234"):
        phone = "234" + phone

    return phone
