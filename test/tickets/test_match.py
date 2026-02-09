import datetime

import pytest

from domain.enum import RouteType
from domain.route import RouteConfig
from domain.ticket import TicketComplete
from tickets.match import match_ticket_route


@pytest.mark.parametrize(
    "ticket, route, result",
    [
        [
            TicketComplete(
                id=1,
                chat_id=1,
                chat_name="test",
                message_id=1,
                posted_at=datetime.datetime(2026, 2, 1, tzinfo=datetime.UTC),
                route_from="Almaty",
                route_to="Danang",
                date_start=datetime.datetime(2026, 2, 3, tzinfo=datetime.UTC),
                date_end=None,
                price=18500,
                currency="rub",
                airline="Aeroflot",
            ),
            RouteConfig(
                username="Eldars",
                chat_id=123,
                routes_from=["Almaty"],
                routes_to=["Danang"],
                date_start=datetime.date(2026, 2, 2),
                date_end=datetime.date(2026, 2, 10),
                route_type=RouteType.one_way,
            ),
            True,
        ],
        [
            TicketComplete(
                id=1,
                chat_id=1,
                chat_name="test",
                message_id=1,
                posted_at=datetime.datetime(2026, 2, 1, tzinfo=datetime.UTC),
                route_from="Almaty",
                route_to="Danang",
                date_start=datetime.datetime(2026, 2, 2, tzinfo=datetime.UTC),
                date_end=None,
                price=18500,
                currency="rub",
                airline="Aeroflot",
            ),
            RouteConfig(
                username="Eldars",
                chat_id=123,
                routes_from=["Almaty"],
                routes_to=["Danang"],
                date_start=datetime.date(2026, 2, 2),
                date_end=datetime.date(2026, 2, 10),
                route_type=RouteType["one_way"],
            ),
            True,
        ],
        [
            TicketComplete(
                id=1,
                chat_id=1,
                chat_name="test",
                message_id=1,
                posted_at=datetime.datetime(2026, 2, 1, tzinfo=datetime.UTC),
                route_from="Almaty",
                route_to="Danang",
                date_start=datetime.datetime(2026, 2, 3, tzinfo=datetime.UTC),
                date_end=None,
                price=18500,
                currency="rub",
                airline="Aeroflot",
            ),
            RouteConfig(
                username="Eldars",
                chat_id=123,
                routes_from=["Almaty"],
                routes_to=["Danang"],
                date_start=datetime.date(2026, 2, 4),
                date_end=datetime.date(2026, 2, 10),
                route_type=RouteType["one_way"],
            ),
            False,
        ],
    ],
)
def test_match_ticket_route(
    ticket: TicketComplete, route: RouteConfig, result: bool
) -> None:
    actual = match_ticket_route(ticket, route)
    assert actual == result
