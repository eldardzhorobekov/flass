import datetime
from typing import Any

from domain.ticket import Ticket
from parser.date import parse_ambiguous_date
from pkg.iata.iata_to_ru import ru_or_en_to_iata


def convert_ai_response_to_ticket(
    data_dict: dict[str, Any], today: datetime.datetime
) -> Ticket:
    date_start = __choose_nearest_future_date(
        data_dict["date_start"], data_dict["date_start_raw"], today
    )
    date_end = (
        __choose_nearest_future_date(
            data_dict["date_end"], data_dict["date_end_raw"], today
        )
        if data_dict["date_end"]
        else None
    )

    ticket = Ticket(
        route_from=ru_or_en_to_iata(data_dict["route_from"]),
        route_to=ru_or_en_to_iata(data_dict["route_to"]),
        date_start=date_start,
        date_end=date_end,
        price=data_dict["price"],
        currency=data_dict["currency"],
        airline=data_dict["airline"],
    )
    return ticket


def __choose_nearest_future_date(
    date: str, date_raw: str, today: datetime.datetime
) -> datetime:
    """
    param:date in "%Y-%m-%dT%H:%M:%S" format
    param:date_raw in MM.DD or DD.MM format

    Return: neares future date to param:today
    """
    candidates = [
        datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").replace(
            tzinfo=datetime.UTC
        ),
        parse_ambiguous_date(date_raw, today),
    ]
    candidates = [c for c in candidates if c and c > today]
    return min(candidates)
