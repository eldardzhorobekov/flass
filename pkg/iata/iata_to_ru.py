# [IATA, Russian Name, English Name]
import re

CITY_DATA = [
    ["ALA", "Алматы", "Almaty"],
    ["NQZ", "Астана", "Astana"],
    ["SCO", "Актау", "Aktau"],
    ["CIT", "Шымкент", "Shymkent"],
    ["GUW", "Атырау", "Atyrau"],
    ["AKX", "Актобе", "Aktobe"],
    ["KGF", "Караганда", "Karaganda"],
    ["KSN", "Костанай", "Kostanay"],
    ["DAD", "Дананг", "Danang"],
    ["CXR", "Нячанг", "Nha Trang"],
    ["CXR", "Камрань", "Cam Ranh"],
    ["PQC", "Фукуок", "Phu Quoc"],
    ["SGN", "Хошимин", "Ho Chi Minh"],
    ["HKT", "Пхукет", "Phuket"],
    ["BKK", "Бангкок", "Bangkok"],
    ["UTP", "Паттайя", "Pattaya"],
    ["SYX", "Санья", "Sanya"],
    ["DPS", "Бали", "Bali"],
    ["DXB", "Дубай", "Dubai"],
    ["DWC", "Дубай (Аль-Мактум)", "Dubai Al Maktoum"],
    ["SHJ", "Шарджа", "Sharjah"],
    ["AUH", "Абу-Даби", "Abu Dhabi"],
    ["AYT", "Анталья", "Antalya"],
    ["IST", "Стамбул", "Istanbul"],
    ["SAW", "Стамбул (Сабиха)", "Istanbul Sabiha"],
    ["PME", "Бодрум", "Bodrum"],
    ["DLM", "Даламан", "Dalaman"],
    ["SSH", "Шарм-эль-Шейх", "Sharm El Sheikh"],
    ["HRG", "Хургада", "Hurghada"],
    ["MCT", "Маскат", "Muscat"],
    ["TBS", "Тбилиси", "Tbilisi"],
    ["BUS", "Батуми", "Batumi"],
    ["EVN", "Ереван", "Yerevan"],
    ["GYD", "Баку", "Baku"],
    ["TAS", "Ташкент", "Tashkent"],
    ["MOW", "Москва", "Moscow"],
    ["LED", "Санкт-Петербург", "Saint Petersburg"],
    ["MIN", "Минск", "Minsk"],
    ["WAW", "Варшава", "Warsaw"],
    ["MIL", "Милан", "Milan"],
]

# 1. IATA_TO_RU: Only sets the value if it doesn't exist yet (keeps the first/primary name)
IATA_TO_RU = {item[0]: item[1] for item in CITY_DATA}
IATA_TO_RU = {}
for code, ru_name, en_name in CITY_DATA:
    if code not in IATA_TO_RU:
        IATA_TO_RU[code] = ru_name
RU_TO_IATA = {item[1].capitalize(): item[0] for item in CITY_DATA}
EN_TO_IATA = {item[2].capitalize(): item[0] for item in CITY_DATA}


def iata_to_ru(iata_code: str) -> str:
    return IATA_TO_RU.get(iata_code.upper(), iata_code)


def ru_or_en_to_iata(city: str) -> str:
    # if IATA in this city string, eg. Almaty (ALA), Moscow (MOW)
    bracket_match = re.search(r"\(([A-Z]{3})\)", city.upper())
    if bracket_match:
        return bracket_match.group(1)

    city = city.capitalize()
    if city in RU_TO_IATA:
        return RU_TO_IATA[city]
    if city in EN_TO_IATA:
        return EN_TO_IATA[city]
    return city
