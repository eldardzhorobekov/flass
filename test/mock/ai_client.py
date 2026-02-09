import json

from clients.openai.request import AIClientBase


class MockOpenAIClient(AIClientBase):
    def request(self, user_content: str, system_content: str) -> str:
        return json.dumps(
            {
                "route_from": "Almaty",
                "route_to": "Danang",
                "date_start": "2026-02-03T00:00:00",
                "date_end": "2026-02-10T00:00:00",
                "price": 18500,
                "currency": "kzt",
                "airline": "Aeroflot",
            }
        )
