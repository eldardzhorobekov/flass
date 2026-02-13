import builtins
import datetime
from collections import defaultdict

from db.tickets.repo import TicketRepo
from domain.enum import RouteType
from domain.route import RouteConfig
from domain.ticket import Ticket, TicketComplete, TicketExists
from tickets.match import match_ticket_route


class TicketController:
    def __init__(self, ticket_repo: TicketRepo) -> None:
        self._ticket_repo = ticket_repo

    async def exists(self, ticket: TicketExists) -> bool:
        return await self._ticket_repo.exists(ticket)

    async def insert(
        self,
        tickets: list[Ticket],
        chat_id: int,
        message_id: int,
        username: str,
        posted_at: datetime.datetime,
    ) -> list[int]:
        ticket_ids = await self._ticket_repo.insert(
            tickets, chat_id, message_id, username, posted_at
        )
        return ticket_ids

    async def list_by_route(self, route: RouteConfig) -> list[TicketComplete]:
        if route.route_type not in (RouteType.one_way,):
            return []

        tickets = await self._ticket_repo.list(route, None)
        tickets = self._filter_tickets_by_last_added(tickets)
        tickets = [t for t in tickets if match_ticket_route(t, route)]
        tickets = sorted(tickets, key=lambda t: (t.price, t.date_start))
        return tickets

    async def list_by_ids(
        self, ids: list[int], route_configs: list[RouteConfig]
    ) -> dict[RouteConfig, list[TicketComplete]]:
        tickets = await self._ticket_repo.list(None, ids)
        tickets = self._filter_tickets_by_last_added(tickets)
        tickets = sorted(tickets, key=lambda t: (t.price, t.date_start))

        route_configs_to_tickets: dict[RouteConfig, list[TicketComplete]] = defaultdict(
            list
        )

        for ticket in tickets:
            for route in route_configs:
                if not match_ticket_route(ticket, route):
                    continue
                route_configs_to_tickets[route].append(ticket)
        return route_configs_to_tickets

    @staticmethod
    def _filter_tickets_by_last_added(
        input_tickets: builtins.list[TicketComplete],
    ) -> builtins.list[TicketComplete]:
        d = defaultdict(list)
        for t in input_tickets:
            t_key = (t.route_from, t.route_to, t.date_start, t.date_end)
            d[t_key].append(t)
        res = []
        for t_key, tickets in d.items():
            last = max(tickets, key=lambda t: t.posted_at)
            res.append(last)
        return res
