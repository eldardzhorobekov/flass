import datetime

import pytest

from db.tickets.repo import TicketRepo
from domain.enum import RouteType
from domain.ticket import ParamsTicketList, Ticket, TicketExists
from pkg.postgre.postgre import PostgreDB


@pytest.mark.asyncio
async def test_repo():
    client = TicketRepo(
        PostgreDB("postgresql://flass_user:password@localhost:5432/flass")
    )  # TODO: move to conftest as test db

    # Example data with actual datetime objects
    test_tickets_to_insert = [
        Ticket(
            "Phuket",
            "Moscow",
            datetime.datetime(2024, 2, 1, tzinfo=datetime.UTC),  # date_start
            None,  # date_end (Optional)
            18500,
            "RUB",
            "Aeroflot",
        ),
        Ticket(
            "Phuket",
            "Almaty",
            datetime.datetime(
                2024, 2, 5, 10, 30, tzinfo=datetime.UTC
            ),  # date_start with time
            datetime.datetime(2024, 2, 15, tzinfo=datetime.UTC),  # date_end (Optional)
            12000,
            "RUB",
            None,
        ),
    ]

    ticket_ids = await client.insert(
        test_tickets_to_insert, 99, 100, "test", datetime.datetime(2026, 2, 7)
    )

    for t in ticket_ids:
        ticket = await client.get(t)

    exist_test_cases = [
        [
            TicketExists(
                "Phuket",
                "Moscow",
                test_tickets_to_insert[0].date_start,
                test_tickets_to_insert[0].date_end,
                test_tickets_to_insert[0].airline,
            ),
            True,
        ],
        [
            TicketExists(
                "Phuket",
                "Almaty",
                test_tickets_to_insert[1].date_start,
                test_tickets_to_insert[1].date_end,
                test_tickets_to_insert[1].airline,
            ),
            True,
        ],
        [
            TicketExists(
                "Phuket",
                "Bishkek",
                test_tickets_to_insert[1].date_start,
                test_tickets_to_insert[1].date_end,
                test_tickets_to_insert[1].airline,
            ),
            False,
        ],
    ]
    for ticket, expected in exist_test_cases:
        actual = await client.exists(ticket)
        assert expected == actual

    list_tickets_test_cases = [
        [
            ParamsTicketList(
                routes_from=["Phuket"],
                routes_to=["Moscow"],
                date_start=test_tickets_to_insert[0].date_start,
                date_end=test_tickets_to_insert[0].date_end,
                route_type=RouteType.one_way,
            ),
            1,
        ],
        [
            ParamsTicketList(
                routes_from=["Phuket"],
                routes_to=["New York"],
                date_start=test_tickets_to_insert[0].date_start,
                date_end=test_tickets_to_insert[0].date_end,
                route_type=RouteType.one_way,
            ),
            0,
        ],
    ]

    for params, has_at_least in list_tickets_test_cases:
        listed_tickets = await client.list(params)
        assert len(listed_tickets) >= has_at_least, params
