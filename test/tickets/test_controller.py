import datetime

from tickets.controller import TicketController


def test__filter_tickets_by_last_added(ticket_factory):
    chat_id = 1
    utc = datetime.UTC
    airline = "Aeroflot"  # Фиксируем авиакомпанию для всех

    # Almaty - Danang
    ala_1 = ticket_factory(
        route_from="Almaty",
        route_to="Danang",
        price=18500,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 1, 28, tzinfo=utc),
    )
    ala_2 = ticket_factory(
        route_from="Almaty",
        route_to="Danang",
        price=15000,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 1, 31, tzinfo=utc),
    )
    ala_last = ticket_factory(
        route_from="Almaty",
        route_to="Danang",
        price=13000,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 2, 1, tzinfo=utc),
    )

    # Bishkek - Phuquoc
    bish_1 = ticket_factory(
        route_from="Bishkek",
        route_to="Phuquoc",
        price=15000,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 1, 28, tzinfo=utc),
    )
    bish_last = ticket_factory(
        route_from="Bishkek",
        route_to="Phuquoc",
        price=20000,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 2, 5, tzinfo=utc),
    )

    # Moscow - Phuket
    mos_last = ticket_factory(
        route_from="Moscow",
        route_to="Phuket",
        price=50000,
        chat_id=chat_id,
        airline=airline,
        posted_at=datetime.datetime(2026, 2, 5, tzinfo=utc),
    )

    tickets = [ala_1, ala_2, ala_last, bish_1, bish_last, mos_last]

    # Ожидаем только последние билеты с проставленными ценами
    ala_last.prev_price = 15000
    bish_last.prev_price = 15000
    mos_last.prev_price = None

    expected = [ala_last, bish_last, mos_last]

    actual = TicketController._filter_tickets_by_last_added(tickets)

    # Сортировка важна для сравнения списков
    actual.sort(key=lambda x: (x.route_from, x.route_to))
    expected.sort(key=lambda x: (x.route_from, x.route_to))

    assert actual == expected


def test_filter_ignores_same_price(ticket_factory):
    # Создаем три билета: 100к -> 100к -> 90к
    t1 = ticket_factory(price=100000)
    t1.posted_at = datetime.datetime(2026, 2, 1, 10, 0)

    t2 = ticket_factory(price=100000)
    t2.posted_at = datetime.datetime(2026, 2, 1, 11, 0)

    t3 = ticket_factory(price=90000)
    t3.posted_at = datetime.datetime(2026, 2, 1, 12, 0)

    from tickets.controller import TicketController

    result = TicketController._filter_tickets_by_last_added([t1, t2, t3])

    assert len(result) == 1
    assert result[0].price == 90000
    assert result[0].prev_price == 100000
