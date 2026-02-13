import datetime
import random
from collections.abc import Callable

import pytest

from tickets.message import TicketComplete

# Тип для подсказок IDE
TicketFactoryType = Callable[..., TicketComplete]


@pytest.fixture
def ticket_factory() -> TicketFactoryType:
    """Фабрика для создания билетов с предсказуемыми дефолтами"""

    def _create_ticket(
        route_from: str = "NQZ",
        route_to: str = "HKT",
        price: int = 100000,
        currency: str = "KZT",
        is_rt: bool = False,
        days_delta: int = 7,
        airline: str | None = None,
        chat_id: int = 1,
        chat_name: str = "test",
        posted_at: datetime.datetime | None = None,
        prev_price: int | None = None,
    ) -> TicketComplete:

        # Если время не задано, используем фиксированное, чтобы тесты не зависели от секунды запуска
        if posted_at is None:
            posted_at = datetime.datetime(2026, 2, 13, 10, 0, tzinfo=datetime.UTC)

        start_date = datetime.datetime(2026, 3, 1, tzinfo=datetime.UTC)
        # Важно: для date_end используем None или datetime (не список!)
        end_date = start_date + datetime.timedelta(days=days_delta) if is_rt else None

        return TicketComplete(
            route_from=route_from,
            route_to=route_to,
            date_start=start_date,
            date_end=end_date,
            price=price,
            currency=currency,
            airline=airline,
            id=random.randint(1, 99999),
            chat_id=chat_id,
            chat_name=chat_name,
            message_id=random.randint(1000, 9999),
            posted_at=posted_at,
            prev_price=prev_price,
        )

    return _create_ticket
