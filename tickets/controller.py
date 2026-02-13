import datetime
from collections import defaultdict

from db.tickets.alchemy_repo import TicketRepository
from db.tickets.repo import TicketRepo
from domain.enum import RouteType
from domain.route import RouteConfig
from domain.ticket import Ticket, TicketComplete, TicketExists
from tickets.match import match_ticket_route


class TicketController:
    def __init__(self, ticket_repo: TicketRepo, alch_repo: TicketRepository) -> None:
        self._ticket_repo = ticket_repo
        self._alch_repo = alch_repo

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

        tickets = await self._ticket_repo.list_tickets(route, None)
        tickets = self._filter_tickets_by_last_added(tickets)
        tickets = [t for t in tickets if match_ticket_route(t, route)]
        tickets = sorted(tickets, key=lambda t: (t.price, t.date_start))
        return tickets

    async def list_by_ids(
        self, ticket_ids: list[int], route_configs: list[RouteConfig]
    ) -> dict[RouteConfig, list[TicketComplete]]:
        new_tickets = await self._ticket_repo.list_tickets(None, ticket_ids)
        if not new_tickets:
            return []
        keys = [
            (t.route_from, t.route_to, t.date_start, t.date_end, t.airline, t.chat_id)
            for t in new_tickets
        ]
        history_tickets = await self._alch_repo.get_latest_by_routes(
            keys, exclude_ids=ticket_ids
        )
        # tickets = self._filter_tickets_by_last_added(new_tickets + history_tickets)
        tickets = self._filter_new_vs_history(new_tickets, history_tickets)
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
        input_tickets: list[TicketComplete],
    ) -> list[TicketComplete]:
        if not input_tickets:
            return []

        # 1. Сортируем по времени публикации
        sorted_tickets = sorted(input_tickets, key=lambda t: t.posted_at)

        # 2. Группируем билеты
        d = defaultdict(list)
        for t in sorted_tickets:
            t_key = (
                t.route_from,
                t.route_to,
                t.date_start,
                t.date_end,
                t.airline,
                t.chat_id,
            )
            d[t_key].append(t)

        res = []
        for tickets in d.values():
            last = tickets[-1]
            last.prev_price = None  # По умолчанию пусто

            # Идем с конца списка к началу, ищем первую цену, которая не равна текущей
            current_price = last.price
            for i in range(len(tickets) - 2, -1, -1):
                if tickets[i].price != current_price:
                    last.prev_price = tickets[i].price
                    break  # Нашли ближайшее изменение — выходим

            res.append(last)
        return res

    @staticmethod
    def _filter_new_vs_history(
        new_tickets: list[TicketComplete], history_tickets: list[TicketComplete]
    ) -> list[TicketComplete]:
        # 1. Группируем историю по ключу, чтобы быстро находить последний билет
        history_map = defaultdict(list)
        # exclude_others
        for t in history_tickets:
            t_key = (
                t.route_from,
                t.route_to,
                t.date_start,
                t.date_end,
                t.airline,
                t.chat_id,
            )
            history_map[t_key].append(t)

        res = []
        for nt in new_tickets:
            nt_key = (
                nt.route_from,
                nt.route_to,
                nt.date_start,
                nt.date_end,
                nt.airline,
                nt.chat_id,
            )

            # Если этого маршрута раньше не было в базе — это 100% новый билет
            if nt_key not in history_map:
                res.append(nt)
                continue

            # Достаем историю для этого конкретного билета и сортируем по времени
            group = sorted(history_map[nt_key], key=lambda t: t.posted_at)
            last_history = group[-1]

            # ГЛАВНОЕ УСЛОВИЕ: если цена в базе такая же, как у нового — скипаем
            if nt.price == last_history.price:
                continue

            # Если цена изменилась, ищем значение для зачеркивания (prev_price)
            # Проходим по истории назад и берем ПЕРВУЮ цену, которая отличается от текущей новой
            for i in range(len(group) - 1, -1, -1):
                if group[i].price != nt.price:
                    nt.prev_price = group[i].price
                    break

            res.append(nt)

        return res
