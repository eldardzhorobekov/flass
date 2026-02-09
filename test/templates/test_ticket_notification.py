import datetime

import pytest

from domain.ticket import TicketComplete
from tickets.message import format_ticket_message


@pytest.mark.parametrize(
    "ticket, expected",
    [
        [
            TicketComplete(
                id=1,
                chat_id=1,
                chat_name="test_chat",
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
            """📍 Almaty — Danang
📅 Вылет: 2026-02-03
💰 Цена: 18500 rub
✈️ Авиакомпания: Aeroflot

[Перейти в чат @test_chat](https://t.me/test_chat/1)""",
        ]
    ],
)
def test_ticket_notification(ticket: TicketComplete, expected: str) -> None:
    actual = format_ticket_message(ticket)
    assert actual == expected
