# IMPORTANT: unused

from parser.charterticketsme import parse_standard_hot

PARSERS = [parse_standard_hot]


def extract_data(text: str) -> dict[str, str]:
    for parser in PARSERS:
        result = parser(text)
        if result:
            return result
    return {"error": "No matching format found"}
