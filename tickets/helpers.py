import re


def is_likely_ticket(text: str) -> bool:
    """
    Returns True if the message contains patterns typical for
    Kazakhstan/CIS flight Telegram channels (Dates, Prices, Routes).
    """
    # 1. Look for Date patterns: 30.01, 08.02, etc.
    date_pattern = r"\d{2}\.\d{2}"

    # 2(\d{1,3}(?:[\s\.]\d{3})+) -> Matches grouped numbers like 240 000, 1.500.000, 10 000 000
    # |                        -> OR
    # (\d{4,})                 -> Matches any standalone number with 4 or more digits (e.g., 5000, 100000)
    # may match year or phone number, but that's okay
    price_pattern = r"(\d{1,3}(?:[\s\.]\d{3})+|\d{4,})"

    # 3. Look for Route indicators: Dash between capitalized words or " - "
    # This helps catch "Алматы - Санья"
    city_word = r"[А-ЯЁA-Z][а-яёa-z]+"
    route_pattern = rf"{city_word}\s?[-—–<>]+\s?{city_word}"

    # Check for matches
    has_date = re.search(date_pattern, text) is not None
    has_price = re.search(price_pattern, text.lower()) is not None
    has_route = re.search(route_pattern, text) is not None

    # Logic: It's likely a ticket if it has a route AND (a date OR a price)
    # This filters out random chat messages while keeping "A - B" offers.
    return has_route or has_date or has_price
