import json
import logging
from asyncio import Queue

from telethon import TelegramClient, events

from clients.openai.request import OpenAIClient
from clients.telegram.get_username import get_username
from tickets.controller import TicketController
from tickets.convert import convert_ai_response_to_ticket
from tickets.helpers import is_likely_ticket

PROMPT = """
### ROLE
You are a travel data extraction agent for the Kazakhstan/CIS market. Your task is to extract flight deal information from Telegram messages and return a JSON list of flight objects.

### CONSTRAINTS
- ALWAYS return a valid JSON list of objects: [{}, {}].
- If no flights are found, return: [{"error": true, "reason": "No flight data detected"}]
- TODAY'S DATE: 2026-02-05. Use this to resolve relative dates (e.g., "tomorrow").
- AIRLINES: Map 'S' to 'Scat', 'A' to 'Air Astana', 'V' to 'Vietjet'. Use the full name in the "airline" field.
- DATES: 
    - Provide full ISO 8601 format: YYYY-MM-DDTHH:MM:SS.
    - Default time to 00:00:00 if not specified in the text.
    - Don't specify the offset
- PRICE: Extract as a pure number.
- CURRENCY: Use ISO 4217 (e.g., 185000 ₸ = KZT, $400 = USD).

### OUTPUT SCHEMA
{
    "flights": [],
    "error": bool,
    "error_text": text,
}

Each object must contain:
{
  "route_from": "string (original text)",
  "route_to": "string (original text)",
  "date_start": "string (YYYY-MM-DDTHH:MM:SS)",
  "date_end": "string (YYYY-MM-DDTHH:MM:SS) or null",
  "date_start_raw": "string (original text)",
  "date_end_raw": "string (original text) or null",
  "price": "number",
  "currency": "string (ISO 4217)",
  "airline": "string (Full Name)"
}
"""

logger = logging.getLogger(__name__)


async def read_chats(
    queue: Queue,
    tg_client: TelegramClient,
    openai_client: OpenAIClient,
    ticket_ctrl: TicketController,
    target_chats: list[str],
) -> None:
    @tg_client.on(events.NewMessage(chats=target_chats))
    async def reading_ticket_chats(event: events.NewMessage.Event):
        logger.debug(f"[{event.chat.title}] New Post: {event.text}")
        if not is_likely_ticket(event.text):
            logger.warning(f"Not a ticket. Message ID={event.id}, Text={event.text}")
            return
        username = await get_username(event)
        resp_str = openai_client.request(
            user_content=event.text,
            system_content=PROMPT,
        )
        data_dict = json.loads(resp_str)
        if data_dict.get("error") or "flights" not in data_dict:
            logger.error(f"skipping AI error response: {resp_str}")
            return
        logger.info(f"AI response: {resp_str}")
        try:
            tickets = [
                convert_ai_response_to_ticket(d, event.date)
                for d in data_dict["flights"]
            ]
        except ValueError as e:
            logger.error(f"can't convert resp to Ticket. resp: {resp_str}. error: {e}")
            return

        try:
            ticket_ids = await ticket_ctrl.insert(
                tickets, event.chat.id, event.message.id, username, event.message.date
            )
            for t in ticket_ids:
                await queue.put(t)
        except Exception as e:
            logger.error(f"can't insert tickets to db: {tickets}. Error: {e}")
            return

    try:
        # This keeps the script running until you kill it or it loses connection
        logger.info(f"Reading chats {target_chats}")
        await tg_client.start()
        logger.debug("Bot is running...")
        await tg_client.run_until_disconnected()
    finally:
        # This block ALWAYS runs, even if the script crashes or you press Ctrl+C
        logger.info("\nShutting down Flass project...")

        # 1. Disconnect from Telegram servers safely
        await tg_client.disconnect()

        # 2. Close your Postgres connection/pool
        # db.close()

        logger.info("All systems closed. Data is safe.")
