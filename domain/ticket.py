import datetime
from dataclasses import dataclass

from domain.enum import RouteType


@dataclass
class Ticket:
    route_from: str
    route_to: str
    date_start: datetime.datetime
    date_end: datetime.datetime | None
    price: int
    currency: str
    airline: str | None


@dataclass
class TicketComplete(Ticket):
    id: int
    chat_id: int
    chat_name: str
    message_id: int
    posted_at: datetime.datetime
    prev_price: int | None = None


@dataclass
class TicketExists:
    route_from: str
    route_to: str
    date_start: datetime.datetime
    date_end: datetime.datetime | None
    airline: str | None


@dataclass
class ParamsTicketList:
    routes_from: list[str]
    routes_to: list[str]
    date_start: datetime.datetime
    date_end: datetime.datetime
    route_type: RouteType
