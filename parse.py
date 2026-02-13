import json
import logging
import os
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from telethon import TelegramClient

from clients.openai.request import OpenAIClient
from clients.telegram.get_username import get_username
from configs.logger import setup_logger
from db.tickets.repo import TicketRepo
from pkg.postgre.postgre import PostgreDB
from tickets.controller import TicketController
from tickets.convert import convert_ai_response_to_ticket
from tickets.helpers import is_likely_ticket
from tickets.read_chats import PROMPT

load_dotenv()
setup_logger(os.getenv("LOG_LEVEL", logging.INFO))
logger = logging.getLogger(__name__)
TG_API_SESSION_NAME = os.getenv("TG_API_SESSION_NAME")
TG_API_ID = int(os.getenv("TG_API_ID"))
TG_API_HASH = os.getenv("TG_API_HASH")
client = TelegramClient(TG_API_SESSION_NAME, TG_API_ID, TG_API_HASH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "db")  # Именно "db", как в docker-compose
db_name = os.getenv("DB_NAME")

# Строка подключения будет выглядеть так:
POSTGRE_DB_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
CHANNELS = os.getenv("TELEGRAM_CHATS").split(",")


async def main():
    # Временная отсечка (2 дня назад)
    offset = datetime.now(UTC) - timedelta(hours=24)

    openai_client = OpenAIClient(OPENAI_API_KEY)
    postgre_db = PostgreDB(db_url=POSTGRE_DB_URL)
    tickets_repo = TicketRepo(postgre_db)
    ticket_ctrl = TicketController(tickets_repo)
    await client.start()

    for channel in CHANNELS:
        print(f"--- Парсим канал: {channel} ---")
        async for message in client.iter_messages(
            channel,
            offset_date=offset,
            reverse=True,
        ):
            logger.debug(f"[{message.chat.title}] New Post: {message.text}")
            if not message.text or not is_likely_ticket(message.text):
                logger.warning(
                    f"Not a ticket. Message ID={message.id}, Text={message.text}"
                )
                continue
            username = await get_username(message)
            resp_str = openai_client.request(
                user_content=message.text,
                system_content=PROMPT,
            )
            data_dict = json.loads(resp_str)
            if data_dict.get("error") or "flights" not in data_dict:
                logger.error(f"skipping AI error response: {resp_str}")
                continue
            logger.info(f"AI response: {resp_str}")
            try:
                tickets = [
                    convert_ai_response_to_ticket(d, message.date)
                    for d in data_dict["flights"]
                ]
            except ValueError as e:
                logger.error(
                    f"can't convert resp to Ticket. resp: {resp_str}. error: {e}"
                )
                continue

            try:
                await ticket_ctrl.insert(
                    tickets,
                    message.chat.id,
                    message.id,
                    username,
                    message.date,
                )
            except Exception as e:
                logger.error(f"can't insert tickets to db: {tickets}. Error: {e}")
                return


with client:
    client.loop.run_until_complete(main())
