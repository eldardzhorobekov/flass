from telethon import events


async def get_username(event: events.NewMessage.Event) -> str:
    chat = await event.get_chat()
    display_name = getattr(chat, "username", None)
    if display_name:
        return display_name
    return getattr(chat, "title", "Private chat")
