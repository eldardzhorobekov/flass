from jinja2 import Environment

from test.templates.conftest import TicketFactoryType
from tickets.message import render_list_tickets


def test_empty_tickets(jinja_env: Environment) -> None:
    """Проверка обработки пустого списка"""
    assert render_list_tickets(jinja_env, []) == "Билетов не найдено."


def test_grouping_by_channels(
    jinja_env: Environment, ticket_factory: TicketFactoryType
) -> None:
    """Проверка, что билеты разделяются по разным каналам"""
    t1 = ticket_factory()
    t1.chat_name = "charter_kz"

    t2 = ticket_factory()
    t2.chat_name = "lowcost_kg"

    result: str = render_list_tickets(jinja_env, [t1, t2])

    assert "КАНАЛ: CHARTER_KZ" in result
    assert "КАНАЛ: LOWCOST_KG" in result
    assert result.count("━━━━━━━━━━━━━━━━━━") == 2


def test_sorting_ow_before_rt(
    jinja_env: Environment, ticket_factory: TicketFactoryType
) -> None:
    """Проверка, что билеты 'в одну сторону' всегда выше 'туда-обратно'"""
    # Создаем RT первым, OW вторым
    rt = ticket_factory(is_rt=True, price=200000)
    ow = ticket_factory(is_rt=False, price=50000)

    # Передаем в перемешанном виде
    result: str = render_list_tickets(jinja_env, [rt, ow])

    # OW должен быть выше RT в тексте
    assert result.find("50000") < result.find("200000")


def test_round_trip_nights_calculation(
    jinja_env: Environment, ticket_factory: TicketFactoryType
) -> None:
    """Проверка корректности отображения маршрута и ночей для RT"""
    days = 12
    ticket = ticket_factory(
        is_rt=True, route_from="NQZ", route_to="DAD", days_delta=days
    )

    result: str = render_list_tickets(jinja_env, [ticket])

    assert "📍 Астана ➔ Дананг ➔ Астана" in result
    assert f"({days}н)" in result
    assert "💰" in result


def test_message_link_construction(
    jinja_env: Environment, ticket_factory: TicketFactoryType
) -> None:
    """Проверка правильности формирования ссылки на пост в Telegram"""
    chat = "my_travel_bot"
    msg_id = 777
    ticket = ticket_factory()
    ticket.chat_name = chat
    ticket.message_id = msg_id

    result: str = render_list_tickets(jinja_env, [ticket])

    expected_link = f"https://t.me/{chat}/{msg_id}"
    assert expected_link in result


def test_multiple_routes_in_one_channel(
    jinja_env: Environment, ticket_factory: TicketFactoryType
) -> None:
    """Проверка, что разные направления в одном канале группируются отдельно"""
    t1 = ticket_factory(route_from="ALA", route_to="HKT")
    t2 = ticket_factory(route_from="NQZ", route_to="DAD")

    result: str = render_list_tickets(jinja_env, [t1, t2])

    assert "📍 Алматы ➔ Пхукет" in result
    assert "📍 Астана ➔ Дананг" in result
    # Проверяем, что заголовок канала только один
    assert result.count("КАНАЛ:") == 1
