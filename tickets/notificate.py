import logging

from jinja2 import Environment
from telethon import TelegramClient

from domain.ticket import TicketComplete
from tickets.message import render_list_tickets

logger = logging.getLogger(__name__)


class TicketNotificateClient:
    def __init__(self, tg_bot: TelegramClient) -> None:
        self._tg_bot = tg_bot
        self._sent_messages_cache = set()  # TODO: make fault-tolerant, maybe use redis

    async def notificate_v2(
        self, jinja_env: Environment, chat_id: int, tickets: list[TicketComplete]
    ) -> bool:
        filtered_tickets = []
        for ticket in tickets:
            cache_key = f"{ticket.id}_{chat_id}"
            if cache_key in self._sent_messages_cache:
                continue
            self._sent_messages_cache.add(cache_key)
            filtered_tickets.append(ticket)

        message = render_list_tickets(jinja_env, filtered_tickets)
        logger.debug(f"sending message. chat_id:{chat_id}, message:\n{message}")
        await self._tg_bot.send_message(
            chat_id, message=message, link_preview=False, parse_mode="Markdown"
        )
