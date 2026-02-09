import datetime
from dataclasses import dataclass
from typing import Any

from domain.enum import RouteType


@dataclass
class RouteConfig:
    username: str
    chat_id: int
    routes_from: list[str]
    routes_to: list[str]
    date_start: datetime.date
    date_end: datetime.date
    route_type: RouteType

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RouteConfig":
        return cls(
            username=data["username"],
            chat_id=data["chat_id"],
            routes_from=data["routes_from"],
            routes_to=data["routes_to"],
            date_start=datetime.datetime.strptime(
                data["date_start"], "%Y-%m-%d"
            ).date(),
            date_end=datetime.datetime.strptime(data["date_end"], "%Y-%m-%d").date(),
            route_type=RouteType[data["route_type"]],
        )
