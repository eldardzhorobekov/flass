import logging

from domain.enum import RouteType
from domain.route import RouteConfig
from domain.ticket import TicketComplete

logger = logging.getLogger(__name__)


def match_ticket_route(ticket: TicketComplete, route: RouteConfig) -> bool:
    if (
        ticket.route_from not in route.routes_from
        or ticket.route_to not in route.routes_to
    ):
        logger.debug(
            f"missmatch: ID={ticket.id}, {ticket.route_from}, {route.routes_from}, {ticket.route_to}, {route.routes_to}",
        )
        return False
    if route.route_type == RouteType.one_way:
        if not (route.date_start <= ticket.date_start.date() <= route.date_end):
            logger.debug(
                f"missmatch: {route.date_start}, {ticket.date_start.date()}, {route.date_end}",
            )
            return False
        return True
    raise NotImplementedError(f"RouteType {route.route_type} not implemented")
