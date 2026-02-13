from jinja2 import Environment

from domain.route import RouteConfig
from domain.ticket import TicketComplete
from pkg.iata.iata_to_ru import iata_to_ru
from templates.ticket_notification import (
    CONFIG_TEMPLATE,
    USER_NOTIFICATION_TEMPLATE,
)


def format_ticket_message(ticket: TicketComplete) -> str:
    return USER_NOTIFICATION_TEMPLATE.format(
        route_from=iata_to_ru(ticket.route_from),
        route_to=iata_to_ru(ticket.route_to),
        date_start=f"{ticket.date_start:%Y-%m-%d}",
        price=ticket.price,
        currency=ticket.currency,
        airline=ticket.airline,
        chat_name=ticket.chat_name,
        message_id=ticket.message_id,
    )


def format_route_config_message(config: RouteConfig) -> str:
    return CONFIG_TEMPLATE.format(
        routes_from=" | ".join(iata_to_ru(r) for r in config.routes_from),
        routes_to=" | ".join(iata_to_ru(r) for r in config.routes_to),
        date_start=config.date_start.strftime("%m.%d.%Y"),
        date_end=config.date_end.strftime("%m.%d.%Y"),
    )


def render_list_tickets(jinja_env: Environment, tickets: list[TicketComplete]):
    if not tickets:
        return "Билетов не найдено."

    # Подготовка и сортировка
    for t in tickets:
        t.group_key_simple = f"{t.route_from}-{t.route_to}"

    # Сортировка: чат -> тип (OW/RT) -> дата
    tickets.sort(key=lambda x: (x.chat_name, x.date_end is not None, x.date_start))

    template = jinja_env.get_template("list_tickets.j2")
    return template.render(tickets=tickets)
