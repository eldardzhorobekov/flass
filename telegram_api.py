import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

# Use your own values from my.telegram.org
api_id = os.getenv("FLASS_BOT_API_ID")
api_hash = os.getenv("FLASS_BOT_API_HASH")

client = TelegramClient("anon", api_id, api_hash)


@client.on(events.NewMessage(chats=["@test_e2dar"]))
async def handler(event):
    print(f"New message in {event.chat_id}: {event.text}")


print("Listening for messages...")
client.start()
client.run_until_disconnected()
