import datetime

import pytest

from db.models import TicketModel
from db.tickets.alchemy_repo import TicketRepository


@pytest.mark.asyncio
async def test_get_latest_by_routes(db_session):
    repo = TicketRepository(db_session)
    utc = datetime.UTC

    # Ключ, по которому будем искать
    route_key = (
        "ALA",
        "DAD",
        datetime.datetime(2026, 3, 1, tzinfo=utc),
        None,
        "Aeroflot",
        1,
    )

    # 1. Создаем историю цен (от старых к новым)
    t1 = TicketModel(
        id=1,
        route_from="ALA",
        route_to="DAD",
        date_start=datetime.datetime(2026, 3, 1, tzinfo=utc),
        price=150000,
        airline="Aeroflot",
        chat_id=1,
        chat_name="test",
        message_id=101,
        posted_at=datetime.datetime(2026, 1, 1, tzinfo=utc),
    )
    t2 = TicketModel(
        id=2,
        route_from="ALA",
        route_to="DAD",
        date_start=datetime.datetime(2026, 3, 1, tzinfo=utc),
        price=140000,
        airline="Aeroflot",
        chat_id=1,
        chat_name="test",
        message_id=102,
        posted_at=datetime.datetime(2026, 1, 10, tzinfo=utc),  # Свежее
    )
    t3 = TicketModel(
        id=3,
        route_from="ALA",
        route_to="DAD",
        date_start=datetime.datetime(2026, 3, 1, tzinfo=utc),
        price=130000,
        airline="Aeroflot",
        chat_id=1,
        chat_name="test",
        message_id=103,
        posted_at=datetime.datetime(2026, 1, 20, tzinfo=utc),  # Самый новый
    )

    db_session.add_all([t1, t2, t3])
    await db_session.commit()

    # Сценарий А: Ищем историю для t3, исключая его самого
    # Ожидаем получить t2 (предыдущий по времени)
    keys = [route_key]
    results = await repo.get_latest_by_routes(keys, exclude_ids=[3])

    assert len(results) == 1
    assert results[0].price == 140000
    assert results[0].id == 2

    # Сценарий Б: Ищем историю, исключая t3 и t2
    # Ожидаем получить t1
    results_old = await repo.get_latest_by_routes(keys, exclude_ids=[3, 2])
    assert len(results_old) == 1
    assert results_old[0].id == 1

    # Сценарий В: Передаем пустые ключи
    assert await repo.get_latest_by_routes([], [3]) == []
