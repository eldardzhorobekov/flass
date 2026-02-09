from domain.route import RouteConfig
from domain.ticket import TicketComplete
from pkg.iata.iata_to_ru import get_city_ru
from templates.ticket_notification import CONFIG_TEMPLATE, USER_NOTIFICATION_TEMPLATE


def format_ticket_message(ticket: TicketComplete) -> str:
    return USER_NOTIFICATION_TEMPLATE.format(
        route_from=get_city_ru(ticket.route_from),
        route_to=get_city_ru(ticket.route_to),
        date_start=f"{ticket.date_start:%Y-%m-%d}",
        price=ticket.price,
        currency=ticket.currency,
        airline=ticket.airline,
        chat_name=ticket.chat_name,
        message_id=ticket.message_id,
    )


def format_route_config_message(config: RouteConfig) -> str:
    return CONFIG_TEMPLATE.format(
        routes_from=" | ".join(get_city_ru(r) for r in config.routes_from),
        routes_to=" | ".join(get_city_ru(r) for r in config.routes_to),
        date_start=config.date_start.strftime("%m.%d.%Y"),
        date_end=config.date_end.strftime("%m.%d.%Y"),
    )
