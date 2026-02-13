import datetime
from typing import Any

import pytest

from domain.enum import RouteType
from domain.route import RouteConfig
from domain.ticket import Ticket
from pkg.iata.iata_to_ru import iata_to_ru, ru_or_en_to_iata
from tickets.convert import __choose_nearest_future_date, convert_ai_response_to_ticket


@pytest.mark.parametrize(
    "resp_json, today, result",
    [
        [
            {
                "route_from": "Алматы",
                "route_to": "Дубай",
                "date_start": "2023-10-02T01:30:00",
                "date_start_raw": "2023-10-02",
                "date_end": None,
                "date_end_raw": None,
                "price": 18500,
                "currency": "rub",
                "airline": "Aeroflot",
            },
            datetime.datetime(2023, 9, 10, tzinfo=datetime.UTC),
            Ticket(
                route_from="ALA",
                route_to="DXB",
                date_start=datetime.datetime(2023, 10, 2, 1, 30, tzinfo=datetime.UTC),
                date_end=None,
                price=18500,
                currency="rub",
                airline="Aeroflot",
            ),
        ],
    ],
)
def test_convert_ai_response_to_ticket(
    resp_json: dict[str, Any], today: datetime.datetime, result: Ticket
) -> None:
    actual = convert_ai_response_to_ticket(resp_json, today)
    assert actual == result


@pytest.mark.parametrize(
    "date_str, date_str_raw, today, result",
    [
        [
            "2025-12-03T00:00:00",
            "03.12",
            datetime.datetime(2025, 2, 5, tzinfo=datetime.UTC),
            datetime.datetime(2025, 3, 12, tzinfo=datetime.UTC),
        ],
        [
            "2025-12-03T00:00:00",
            "12.03",
            datetime.datetime(2025, 2, 5, tzinfo=datetime.UTC),
            datetime.datetime(2025, 3, 12, tzinfo=datetime.UTC),
        ],
        [
            "2025-03-15T00:00:00",
            "03.15",
            datetime.datetime(2025, 2, 5, tzinfo=datetime.UTC),
            datetime.datetime(2025, 3, 15, tzinfo=datetime.UTC),
        ],
    ],
)
def test___choose_nearest_future_date(
    date_str: str,
    date_str_raw: str,
    today: datetime.datetime,
    result: datetime.datetime,
) -> None:
    actual = __choose_nearest_future_date(date_str, date_str_raw, today)
    assert actual == result


@pytest.mark.parametrize(
    "data, result",
    [
        [
            {
                "username": "Eldars",
                "chat_id": 123,
                "routes_from": ["Almaty"],
                "routes_to": ["Danang"],
                "date_start": "2026-02-03",
                "date_end": "2026-02-10",
                "route_type": "one_way",
            },
            RouteConfig(
                username="Eldars",
                chat_id=123,
                routes_from=("Almaty",),
                routes_to=("Danang",),
                date_start=datetime.date(2026, 2, 3),
                date_end=datetime.date(2026, 2, 10),
                route_type=RouteType.one_way,
            ),
        ]
    ],
)
def test_convert_route_config(data: dict[str, Any], result: RouteConfig) -> None:
    actual = RouteConfig.from_dict(data)
    assert actual == result


@pytest.mark.parametrize(
    "iata_code, expected",
    [["DXB", "Дубай"], ["ALA", "Алматы"], ["XYZ", "XYZ"], ["CXR", "Нячанг"]],
)
def test_iata_to_ru(iata_code: str, expected: str) -> None:
    actual = iata_to_ru(iata_code)
    assert actual == expected


@pytest.mark.parametrize(
    "city, expected",
    [
        ["Almaty", "ALA"],
        ["Алматы", "ALA"],
        ["Алматы (ALA)", "ALA"],
        ["Unknown", "Unknown"],
    ],
)
def test_ru_or_en_to_iata(city: str, expected: str) -> None:
    actual = ru_or_en_to_iata(city)
    assert actual == expected
