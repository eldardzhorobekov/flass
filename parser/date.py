import datetime
import re


def parse_ambiguous_date(
    date_str: str, today: datetime.datetime
) -> datetime.datetime | None:
    """
    Parses a 'XX.YY' string into the nearest possible future ISO date.
    Considers both DD.MM and MM.DD interpretations.
    """

    # Split the input (handles dots, slashes, or dashes)
    parts = re.split(r"[\.\/-]", date_str)
    if len(parts) != 2:
        return None

    v1, v2 = int(parts[0]), int(parts[1])

    # Generate all valid candidate dates
    # We check this year and next year for both DD.MM and MM.DD
    interpretations = [
        (v1, v2),  # Interpretation A: Day=v1, Month=v2
        (v2, v1),  # Interpretation B: Day=v2, Month=v1
    ]

    candidates = []
    for day, month in interpretations:
        for year in [today.year, today.year + 1]:
            try:
                candidate = datetime.datetime(year, month, day, tzinfo=datetime.UTC)
                # Only keep dates that are today or in the future
                if candidate >= today:
                    candidates.append(candidate)
            except ValueError:
                # Skip invalid dates (e.g., 31.02)
                continue

    if not candidates:
        return None

    # Return the minimum (closest) future date
    return min(candidates)
