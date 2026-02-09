import datetime

import pytest

from domain.ticket import TicketComplete
from tickets.controller import TicketController


def _last_tickets() -> list[TicketComplete]:
    "just don't wanna copy"
    return [
        # Almaty - Danang 2026-02-02
        TicketComplete(
            id=3,
            chat_id=1,
            chat_name="test",
            message_id=3,
            posted_at=datetime.datetime(2026, 2, 1, tzinfo=datetime.UTC),
            route_from="Almaty",
            route_to="Danang",
            date_start=datetime.datetime(2026, 2, 2, tzinfo=datetime.UTC),
            date_end=None,
            price=13000,
            currency="rub",
            airline="Aeroflot",
        ),
        # Bishkek - Phuquoc 2026-02-10
        TicketComplete(
            id=5,
            chat_id=1,
            chat_name="test",
            message_id=5,
            posted_at=datetime.datetime(2026, 2, 5, tzinfo=datetime.UTC),
            route_from="Bishkek",
            route_to="Phuquoc",
            date_start=datetime.datetime(2026, 2, 10, tzinfo=datetime.UTC),
            date_end=None,
            price=20000,
            currency="rub",
            airline="Aeroflot",
        ),
        # Moscow - Phuket
        TicketComplete(
            id=6,
            chat_id=1,
            chat_name="test",
            message_id=6,
            posted_at=datetime.datetime(2026, 2, 5, tzinfo=datetime.UTC),
            route_from="Moscow",
            route_to="Phuket",
            date_start=datetime.datetime(2026, 2, 15, tzinfo=datetime.UTC),
            date_end=None,
            price=50000,
            currency="rub",
            airline="Aeroflot",
        ),
    ]


@pytest.mark.parametrize(
    "tickets, expected",
    [
        [
            [
                # Almaty - Danang 2026-02-02
                TicketComplete(
                    id=1,
                    chat_id=1,
                    chat_name="test",
                    message_id=2,
                    posted_at=datetime.datetime(2026, 1, 28, tzinfo=datetime.UTC),
                    route_from="Almaty",
                    route_to="Danang",
                    date_start=datetime.datetime(2026, 2, 2, tzinfo=datetime.UTC),
                    date_end=None,
                    price=18500,
                    currency="rub",
                    airline="Aeroflot",
                ),
                TicketComplete(
                    id=2,
                    chat_id=1,
                    chat_name="test",
                    message_id=2,
                    posted_at=datetime.datetime(2026, 1, 31, tzinfo=datetime.UTC),
                    route_from="Almaty",
                    route_to="Danang",
                    date_start=datetime.datetime(2026, 2, 2, tzinfo=datetime.UTC),
                    date_end=None,
                    price=15000,
                    currency="rub",
                    airline="Aeroflot",
                ),
                _last_tickets()[0],
                # Bishkek - Phuquoc 2026-02-10
                TicketComplete(
                    id=4,
                    chat_id=1,
                    chat_name="test",
                    message_id=4,
                    posted_at=datetime.datetime(2026, 1, 28, tzinfo=datetime.UTC),
                    route_from="Bishkek",
                    route_to="Phuquoc",
                    date_start=datetime.datetime(2026, 2, 10, tzinfo=datetime.UTC),
                    date_end=None,
                    price=15000,
                    currency="rub",
                    airline="Aeroflot",
                ),
                _last_tickets()[1],
                # Moscow - Phuket
                _last_tickets()[2],
            ],
            _last_tickets(),
        ]
    ],
)
def test__filter_tickets_by_last_added(
    tickets: list[TicketComplete], expected: list[TicketComplete]
) -> list[TicketComplete]:
    actual = TicketController._filter_tickets_by_last_added(tickets)
    assert actual == expected
