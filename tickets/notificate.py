import logging

from telethon import TelegramClient

from domain.ticket import TicketComplete
from tickets.message import format_ticket_message

logger = logging.getLogger(__name__)


class TicketNotificateClient:
    def __init__(self, tg_bot: TelegramClient) -> None:
        self._tg_bot = tg_bot
        self._sent_messages_cache = set()  # TODO: make fault-tolerant, maybe use redis

    async def notificate(self, chat_ids: list[str], ticket: TicketComplete) -> bool:
        for chat_id in chat_ids:
            cache_key = f"{ticket.id}_{chat_id}"
            if cache_key in self._sent_messages_cache:
                continue
            try:
                await self._tg_bot.send_message(
                    chat_id, message=format_ticket_message(ticket), link_preview=False
                )

                self._sent_messages_cache.add(cache_key)
                # await db.mark_user_as_notified(ticket_id, user_id)  - maybe

            except Exception as e:
                logger.error(f"[Error] Failed to send to {chat_id}: {e}")

        all_sent = all(
            f"{ticket.id}_{chat_id}" in self._sent_messages_cache
            for chat_id in chat_ids
        )
        return all_sent
