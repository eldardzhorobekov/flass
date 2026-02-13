import json

from clients.openai.request import AIClientBase


class MockOpenAIClient(AIClientBase):
    def request(self, user_content: str, system_content: str) -> str:
        return json.dumps(
            {
                "flights": [
                    {
                        "route_from": "Almaty",
                        "route_to": "Danang",
                        "date_start": "2026-02-10T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.10",
                        "date_end_raw": None,
                        "price": 120000,
                        "currency": "KZT",
                        "airline": "Scat",
                    },
                    {
                        "route_from": "Almaty",
                        "route_to": "Danang",
                        "date_start": "2026-02-15T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.15",
                        "date_end_raw": None,
                        "price": 150000,
                        "currency": "KZT",
                        "airline": "Air Astana",
                    },
                    {
                        "route_from": "Almaty",
                        "route_to": "Danang",
                        "date_start": "2026-02-08T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.08",
                        "date_end_raw": None,
                        "price": 500000,
                        "currency": "KZT",
                        "airline": "Vietjet",
                    },
                    {
                        "route_from": "Almaty",
                        "route_to": "Nha Trang",
                        "date_start": "2026-02-11T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.11",
                        "date_end_raw": None,
                        "price": 100000,
                        "currency": "KZT",
                        "airline": "Scat",
                    },
                    {
                        "route_from": "Almaty",
                        "route_to": "Nha Trang",
                        "date_start": "2026-02-10T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.10",
                        "date_end_raw": None,
                        "price": 500000,
                        "currency": "KZT",
                        "airline": "Air Astana",
                    },
                    {
                        "route_from": "Almaty",
                        "route_to": "Nha Trang",
                        "date_start": "2026-02-15T00:00:00",
                        "date_end": None,
                        "date_start_raw": "02.15",
                        "date_end_raw": None,
                        "price": 350000,
                        "currency": "KZT",
                        "airline": "Vietjet",
                    },
                ],
                "error": False,
                "error_text": "",
            }
        )
