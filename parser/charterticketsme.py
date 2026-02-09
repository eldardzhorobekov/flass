# IMPORTANT: unused
import re


def parse_standard_hot(text: str) -> dict[str, str]:
    """Matches: 📍 Phuket — Moscow ... 💰 Цена: 18 500 ₽"""
    pattern = r"📍\s*(?P<route>.*)\n.*📅\s*Вылет:\s*(?P<time>.*)\n.*💰\s*Цена:\s*(?P<price>[\d\s]+₽)"
    match = re.search(pattern, text)
    return match.groupdict() if match else None


def parse_two_way(text: str) -> dict[str, str]:
    """
    Алматы - Санья - Алматы
    31.01-08.02 - 185 000 ~~~300 000~~
    Air Astana
    1 место

    Оформление до 15:00 сб
    """
    route_pattern = r"(.+ - .+ - .+)"
    details_pattern = r"(\d{2}\.\d{2})-(\d{2}\.\d{2})\s*-\s*([\d\s]+)"

    route_match = re.search(route_pattern, text)
    details_match = re.search(details_pattern, text)

    if route_match and details_match:
        return {
            "route": route_match.group(1).strip(),
            "date_from": details_match.group(1),
            "date_to": details_match.group(2),
            "price_tenge": details_match.group(3).strip().replace(" ", ""),
        }
    return None
