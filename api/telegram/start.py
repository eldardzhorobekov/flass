from telethon import TelegramClient, events


def register_start_handler(bot: TelegramClient) -> None:
    @bot.on(events.NewMessage(pattern="/start"))
    async def start_handler(event: events.NewMessage.Event) -> None:
        """Handles the /start command."""
        # event.respond sends a message back to the same chat
        await event.respond("Бот активен, отправьте команду /")
