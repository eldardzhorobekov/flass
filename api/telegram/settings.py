import logging

from telethon import TelegramClient, events

from clients.telegram.get_username import get_username

logger = logging.getLogger(__name__)


def register_settings(bot: TelegramClient) -> None:
    @bot.on(events.NewMessage(pattern="/settings"))
    async def start_settings(event: events.NewMessage.Event) -> None:
        """Handles the /settings command."""
        logger.error(
            f"user requested /settings, but it's not implemented yet, user={await get_username(event)}"
        )
        await event.respond("Этот функционал еще не реализован 😇")
