import datetime
from dataclasses import astuple

from domain.ticket import ParamsTicketList, Ticket, TicketComplete, TicketExists
from pkg.postgre.postgre import PostgreDB


class TicketRepo:
    def __init__(self, postgre_client: PostgreDB) -> None:
        self._postgre_client = postgre_client

    async def insert(
        self,
        tickets: list[Ticket],
        chat_id: int,
        message_id: int,
        chat_name: str,
        posted_at: datetime.datetime,
    ) -> list[int]:
        """Safe bulk insert using executemany. Return inserted ticket ids"""
        if not tickets:
            return

        data = [
            (chat_id, chat_name, message_id, posted_at) + astuple(t) for t in tickets
        ]

        columns = "chat_id, chat_name, message_id, posted_at, route_from, route_to, date_start, date_end, price, currency, airline"
        columns_placeholders = ",".join(["%s" for x in columns.split(",")])
        query = f"INSERT INTO flass.tickets ({columns}) VALUES ({columns_placeholders})"
        ticket_ids = await self._postgre_client.execute_many(
            query, data, returning_col="id"
        )
        return ticket_ids

    async def get(self, ticket_id: int) -> TicketComplete:
        query = """
            SELECT id, chat_id, chat_name, message_id, posted_at, route_from, route_to, date_start, date_end, price, currency, airline
            FROM flass.tickets
            WHERE id = %s
        """
        data = await self._postgre_client.fetch_one(query, params=(ticket_id,))
        ticket = TicketComplete(**data)
        return ticket

    async def exists(self, ticket: TicketExists) -> bool:
        and_closes = []  # TODO: use query builder library
        params = [ticket.route_from, ticket.route_to, ticket.date_start]
        if ticket.date_end:
            and_closes.append(" AND date_end = %s")
            params.append(ticket.date_end)
        if ticket.airline:
            and_closes.append(" AND airline = %s")
            params.append(ticket.airline)

        query = f"""
            SELECT EXISTS(
                SELECT 1 
                FROM flass.tickets 
                WHERE route_from = %s
                AND route_to = %s
                AND date_start = %s
                {"".join(and_closes)}
            )
        """

        data = await self._postgre_client.fetch_one(query, params=params)
        return data and data["exists"]

    async def list(self, params: ParamsTicketList) -> list[TicketComplete]:
        query = """
            SELECT id, chat_id, chat_name, message_id, posted_at, route_from, route_to, date_start, date_end, price, currency, airline
            FROM flass.tickets
            WHERE 
            route_from = ANY(%s)
            AND route_to = ANY(%s)
            AND %s <= date_start
        """
        data = await self._postgre_client.fetch_all(
            query, params=[params.routes_from, params.routes_to, params.date_start]
        )
        tickets = [TicketComplete(**d) for d in data]
        return tickets
