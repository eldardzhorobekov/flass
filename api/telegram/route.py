from telethon import TelegramClient, events

from domain.route import RouteConfig
from tickets.message import format_route_config_message


def register_myroute(
    bot: TelegramClient, chat_id_to_route_config: dict[int, RouteConfig]
) -> None:
    @bot.on(events.NewMessage(pattern="/myroute"))
    async def myroute(event: events.NewMessage.Event) -> None:
        """
        Handles the /myroute command. Sends current users route config
        """
        if event.chat_id not in chat_id_to_route_config:
            await event.respond(
                "Не удалось найти ваши настройки. Настройте их здесь: ** /settings **"
            )
            return
        config = chat_id_to_route_config[event.chat_id]
        msg = format_route_config_message(config)
        await event.respond(msg)
