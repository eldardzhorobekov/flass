import logging

import requests

logger = logging.getLogger(__name__)


class TelegramBotClient:
    def __init__(self, token: str) -> None:
        self.__token = token

    async def send_message(self, chat_id: str, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.__token}/sendMessage"
        resp = requests.post(url, json={"chat_id": chat_id, "text": message})
        if resp.status_code != 200:
            logger.error(
                f"can't send a message. Chat ID={chat_id}, Message={message}. Response: {resp.text}"
            )
            return
