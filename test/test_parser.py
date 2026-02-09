import pytest

from tickets.helpers import is_likely_ticket

"""
price_rub
price_kgs
"""


@pytest.mark.parametrize(
    "msg, result",
    [
        [
            """
        Отказные билеты
        Алматы - Санья - Алматы
        30.01 - 07.02 - 240 000 тг
        """,
            True,
        ],
        [
            "How is the weather in Sanya?",
            False,
        ],
        ["Алматы - Фукуок - Алматы\n02.02 - 10.02 - 435 000", True],
        ["30.01 -- Air Astana", True],
        ["Алматы - Фукуок", True],
        ["Алматы -- Фукуок", True],
        ["Алматы --- Фукуок", True],
    ],
)
def test_is_likely_ticket(msg: str, result: bool) -> None:
    actual = is_likely_ticket(msg)
    assert actual == result
