import asyncio
import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient

from api.telegram.list_tickets import register_list_tickets
from api.telegram.route import register_myroute
from api.telegram.settings import register_settings
from api.telegram.start import register_start_handler
from clients.openai.request import OpenAIClient
from configs.logger import setup_logger
from db.tickets.repo import TicketRepo
from domain.route import RouteConfig
from pkg.postgre.postgre import PostgreDB
from pkg.yaml.read import read
from tickets.controller import TicketController
from tickets.match import match_ticket_route
from tickets.notificate import TicketNotificateClient
from tickets.read_chats import read_chats

load_dotenv()
setup_logger(os.getenv("LOG_LEVEL", logging.INFO))
logger = logging.getLogger(__name__)


async def worker_user_notification(
    name: str,
    queue: asyncio.Queue,
    ticket_notificate_client: TicketNotificateClient,
    ticket_repo: TicketRepo,
    route_configs: list[RouteConfig],
) -> None:
    """Processes tickets one by one from the queue."""
    while True:
        ticket_id = await queue.get()
        logger.debug(f"Worker {name} picked up {ticket_id}")

        try:
            ticket = await ticket_repo.get(ticket_id=ticket_id)
            user_chat_ids = []
            for route in route_configs:
                if not match_ticket_route(ticket, route):
                    continue
                user_chat_ids.append(route.chat_id)
            if user_chat_ids:
                logger.debug(
                    f"sending notification to {user_chat_ids}, ticket={ticket.id}"
                )
                await ticket_notificate_client.notificate(user_chat_ids, ticket)
        finally:
            # Notify the queue that the ticket is done
            queue.task_done()


async def main() -> None:
    TG_API_ID = os.getenv("TG_API_ID")
    TG_API_HASH = os.getenv("TG_API_HASH")
    TARGET_CHATS = os.getenv("TELEGRAM_CHATS").split(",")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    POSTGRE_DB_URL = os.getenv("POSTGRE_DB_URL")
    FLASS_BOT_TOKEN = os.getenv("FLASS_BOT_TOKEN")
    FLASS_BOT_API_ID = os.getenv("FLASS_BOT_API_ID")
    FLASS_BOT_API_HASH = os.getenv("FLASS_BOT_API_HASH")

    try:
        route_configs = [
            RouteConfig.from_dict(dict_config)
            for dict_config in read("./route_configs.yaml")["route_configs"]
        ]
    except Exception as e:
        logger.fatal("error reading or converting route configs", f"error: {e}")
        return

    assert TARGET_CHATS != []
    tg_user_client = TelegramClient("testing_session2", TG_API_ID, TG_API_HASH)
    openai_client = OpenAIClient(OPENAI_API_KEY)
    # test_ai_client = MockOpenAIClient()
    postgre_db = PostgreDB(db_url=POSTGRE_DB_URL)
    tickets_repo = TicketRepo(postgre_db)
    ticket_ctrl = TicketController(tickets_repo)

    # START
    flass_bot = TelegramClient("bot_session", FLASS_BOT_API_ID, FLASS_BOT_API_HASH)
    await flass_bot.start(bot_token=FLASS_BOT_TOKEN)

    chat_id_to_route_config = {r.chat_id: r for r in route_configs}

    register_start_handler(flass_bot)
    register_list_tickets(
        bot=flass_bot,
        ticket_controller=ticket_ctrl,
        chat_id_to_route_config=chat_id_to_route_config,
    )
    register_myroute(
        bot=flass_bot,
        chat_id_to_route_config=chat_id_to_route_config,
    )
    register_settings(bot=flass_bot)

    ticket_notificate_client = TicketNotificateClient(flass_bot)
    queue = asyncio.Queue()
    try:
        num_workers = 2

        # Start the worker pool
        workers = []
        for i in range(num_workers):
            worker_task = asyncio.create_task(
                worker_user_notification(
                    f"#{i}",
                    queue,
                    ticket_notificate_client,
                    tickets_repo,
                    route_configs,
                )
            )
            workers.append(worker_task)

        # Start the reader
        reader = asyncio.create_task(
            read_chats(
                queue,
                tg_user_client,
                # test_ai_client,
                openai_client,
                ticket_ctrl,
                TARGET_CHATS,
            )
        )

        # Keep the script running
        await asyncio.gather(reader, *workers)
        await flass_bot.run_until_disconnected()

    except KeyboardInterrupt:
        # Handle the Ctrl+C at the top level
        pass


if __name__ == "__main__":
    logger.debug("App is running...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
