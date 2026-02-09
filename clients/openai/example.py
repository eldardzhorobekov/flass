import datetime
import json
import os

from dotenv import load_dotenv

from clients.openai.request import OpenAIClient
from tickets.convert import convert_ai_response_to_ticket

load_dotenv()

client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))

raw_text = """
Алматы - Санья - Алматы
31.01-08.02 - 185 000 ~~~300 000~~
Air Astana
1 место
"""
raw_text2 = """
Обновления цен
Almaty Phuket
S 12.08 - 120 000
"""
raw_text3 = """
🔥 Ребята, не забывайте подписываться на наш инстаграм! Там мы выкладываем горящие подборки каждые 2 часа. Ссылка в описании профиля.
"""

raw_text4 = """
Обновления цен
Almaty Phuket
S 05.12 - 120 000
"""
PROMPT2 = """
### ROLE
You are a travel data extraction agent for the Kazakhstan/CIS market. Your task is to extract flight deal information from Telegram messages and return a JSON list of flight objects.

### CONSTRAINTS
- ALWAYS return a valid JSON list of objects: [{}, {}].
- If no flights are found, return: [{"error": true, "reason": "No flight data detected"}]
- TODAY'S DATE: 2026-02-05. Use this to resolve relative dates (e.g., "tomorrow").
- IATA CODES: Convert all cities to IATA (e.g., Almaty=ALA, Astana=NQZ, Phuket=HKT).
- AIRLINES: Map 'S' to 'Scat', 'A' to 'Air Astana', 'V' to 'Vietjet'. Use the full name in the "airline" field.
- DATES: 
    - Provide full ISO 8601 format: YYYY-MM-DDTHH:MM:SS.
    - Default time to 00:00:00 if not specified in the text.
    - Don't specify the offset
- PRICE: Extract as a pure number.
- CURRENCY: Use ISO 4217 (e.g., 185000 ₸ = KZT, $400 = USD).

### OUTPUT SCHEMA
{
    "flights": [],
    "error": bool,
    "error_text": text,
}

### PATTERN RECOGNITION
- Look for flight data in these common Telegram structures:
    1. [City] [City] [Airline Code] [Date] - [Price]
    2. [Airline] [Date] - [Price] (Use the message title for route context)
- If a line starts with "S", "A", or "V", it is a FLIGHT.
- If a line contains a date format (DD.MM), it is a FLIGHT.

### FALLBACK LOGIC
- If "route_from" or "route_to" are missing in a specific line, inherit them from the message header or previous line.
- Example: If the header is "Almaty Danang", apply "ALA" and "DAD" to all following price lines.

Each object must contain:
{
  "route_from": "string (IATA)",
  "route_to": "string (IATA)",
  "date_start": "string (YYYY-MM-DDTHH:MM:SS)",
  "date_end": "string (YYYY-MM-DDTHH:MM:SS) or null",
  "date_start_raw": "string (original text)",
  "date_end_raw": "string (original text) or null",
  "price": "number",
  "currency": "string (ISO 4217)",
  "airline": "string (Full Name)"
}
"""
resp = client.request(
    system_content=PROMPT2,
    user_content=raw_text4,
)
# print(resp)
resp_json = json.loads(resp)
print(resp_json)
for f in resp_json["flights"]:
    ticket = convert_ai_response_to_ticket(
        data_dict=f, today=datetime.datetime.now(tz=datetime.UTC)
    )
    print(ticket)
