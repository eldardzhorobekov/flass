from telethon import TelegramClient, events

from domain.route import RouteConfig
from tickets.controller import TicketController
from tickets.message import format_ticket_message


def register_list_tickets(
    bot: TelegramClient,
    ticket_controller: TicketController,
    chat_id_to_route_config: dict[int, RouteConfig],
) -> None:
    @bot.on(events.NewMessage(pattern="/list"))
    async def list_tickets(event: events.NewMessage.Event) -> None:
        """
        Handles the /list command.
        Lists all available tickets by users route config. Sorted by date_start
        """
        # event.respond sends a message back to the same chat
        if event.chat_id not in chat_id_to_route_config:
            await event.respond(
                "Готов к поиску! 🚀 Но сначала мне нужно знать, какие маршруты вас интересуют. Настройте их здесь: ** /settings **"
            )
            return

        tickets = await ticket_controller.list(chat_id_to_route_config[event.chat_id])
        if not tickets:
            await event.respond(
                "На данный момент нет активных билетов по вашему запросу. Настроить другой маршрут: ** /settings **"
            )
            return

        for t in tickets:
            await event.respond(format_ticket_message(t), link_preview=False)
