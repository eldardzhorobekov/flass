import datetime
from dataclasses import dataclass
from typing import Any

from domain.enum import RouteType


@dataclass(frozen=True)
class RouteConfig:
    username: str
    chat_id: int
    routes_from: tuple[str]
    routes_to: tuple[str]
    date_start: datetime.date
    date_end: datetime.date
    route_type: RouteType

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RouteConfig":
        return cls(
            username=data["username"],
            chat_id=data["chat_id"],
            routes_from=tuple(data["routes_from"]),
            routes_to=tuple(data["routes_to"]),
            date_start=datetime.datetime.strptime(
                data["date_start"], "%Y-%m-%d"
            ).date(),
            date_end=datetime.datetime.strptime(data["date_end"], "%Y-%m-%d").date(),
            route_type=RouteType[data["route_type"]],
        )
