import re

# [IATA, Russian Name, English Name]
CITY_DATA = [
    # --- KAZAKHSTAN (Main Hubs) ---
    ["ALA", "Алматы", "Almaty"],
    ["NQZ", "Астана", "Astana"],
    ["CIT", "Шымкент", "Shymkent"],
    ["SCO", "Актау", "Aktau"],
    ["GUW", "Атырау", "Atyrau"],
    ["AKX", "Актобе", "Aktobe"],
    ["UKK", "Усть-Каменогорск", "Oskemen"],
    ["URA", "Уральск", "Oral"],
    ["KGF", "Караганда", "Karaganda"],
    ["KSN", "Костанай", "Kostanay"],
    ["PWQ", "Павлодар", "Pavlodar"],
    ["KZO", "Кызылорда", "Kyzylorda"],
    # --- KYRGYZSTAN ---
    ["FRU", "Бишкек", "Bishkek"],
    ["OSS", "Ош", "Osh"],
    ["IKU", "Тамчы", "Tamchy"],  # Issyk-Kul
    # --- UZBEKISTAN ---
    ["TAS", "Ташкент", "Tashkent"],
    ["SKD", "Самарканд", "Samarkand"],
    ["BHK", "Бухара", "Bukhara"],
    ["UGC", "Ургенч", "Urgench"],
    # --- TAJIKISTAN ---
    ["DYU", "Душанбе", "Dushanbe"],
    ["LBD", "Худжанд", "Khujand"],
    # --- RUSSIA (Major Connections) ---
    ["MOW", "Москва", "Moscow"],  # General code for Moscow
    ["SVO", "Шереметьево", "Sheremetyevo"],
    ["DME", "Домодедово", "Domodedovo"],
    ["VKO", "Внуково", "Vnukovo"],
    ["LED", "Санкт-Петербург", "Saint Petersburg"],
    ["OVB", "Новосибирск", "Novosibirsk"],
    ["SVX", "Екатеринбург", "Yekaterinburg"],
    ["KZN", "Казань", "Kazan"],
    ["AER", "Сочи", "Sochi"],
    # --- TURKEY (Touristic) ---
    ["AYT", "Анталья", "Antalya"],
    ["IST", "Стамбул", "Istanbul"],
    ["SAW", "Сабиха Гёкчен", "Sabiha Gokcen"],
    ["BJV", "Бодрум", "Bodrum"],
    ["DLM", "Даламан", "Dalaman"],
    ["ESB", "Анкара", "Ankara"],
    # --- VIETNAM (Popular Charters) ---
    ["DAD", "Дананг", "Danang"],
    ["CXR", "Нячанг", "Nha Trang"],
    ["CXR", "Камрань", "Cam Ranh"],
    ["PQC", "Фукуок", "Phu Quoc"],
    ["SGN", "Хошимин", "Ho Chi Minh"],
    ["HAN", "Ханой", "Hanoi"],
    # --- THAILAND ---
    ["HKT", "Пхукет", "Phuket"],
    ["BKK", "Бангкок", "Bangkok"],
    ["UTP", "Паттайя", "Pattaya"],
    ["DMK", "Дон Муанг", "Don Mueang"],
    # --- OTHER TOURISTIC (Egypt, UAE, etc.) ---
    ["DXB", "Дубай", "Dubai"],
    ["SHJ", "Шарджа", "Sharjah"],
    ["AUH", "Абу-Даби", "Abu Dhabi"],
    ["SSH", "Шарм-эль-Шейх", "Sharm El Sheikh"],
    ["HRG", "Хургада", "Hurghada"],
    ["MLE", "Мале", "Male"],  # Maldives
    ["DPS", "Бали", "Bali"],
    ["GYD", "Баку", "Baku"],
    ["TBS", "Тбилиси", "Tbilisi"],
    ["BUS", "Батуми", "Batumi"],
    ["EVN", "Ереван", "Yerevan"],
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
