import datetime
from collections.abc import Callable

import pytest
from jinja2 import Environment, FileSystemLoader

from tickets.message import TicketComplete


@pytest.fixture(scope="session")
def jinja_env() -> Environment:
    def iata_to_ru(code: str) -> str:
        mapping: dict[str, str] = {
            "ALA": "Алматы",
            "HKT": "Пхукет",
            "NQZ": "Астана",
            "DAD": "Дананг",
        }
        return mapping.get(code, code)

    env = Environment(
        loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True
    )
    env.filters["iata_to_ru"] = iata_to_ru
    return env


# Определяем тип для фабрики: функция, принимающая аргументы и возвращающая TicketComplete
TicketFactoryType = Callable[..., TicketComplete]


@pytest.fixture
def ticket_factory() -> TicketFactoryType:
    def _create_ticket(
        route_from: str = "NQZ",
        route_to: str = "HKT",
        is_rt: bool = False,
        price: int = 100000,
        days_delta: int = 7,
    ) -> TicketComplete:
        start: datetime.datetime = datetime.datetime(2026, 2, 20)
        end: datetime.datetime | None = (
            start + datetime.timedelta(days=days_delta) if is_rt else None
        )

        return TicketComplete(
            route_from=route_from,
            route_to=route_to,
            date_start=start,
            date_end=end,
            price=price,
            currency="KZT",
            airline=None,
            id=1,
            chat_id=123,
            chat_name="charterkaz",
            message_id=1001,
            posted_at=datetime.datetime.now(),
        )

    return _create_ticket
