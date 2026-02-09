from abc import ABC, abstractmethod

from openai import OpenAI


class AIClientBase(ABC):
    @abstractmethod
    def request(self, user_content: str, system_content: str) -> str:
        pass


class OpenAIClient(AIClientBase):
    def __init__(self, api_key: str) -> None:
        self.__client = OpenAI(api_key=api_key)

    def request(self, user_content: str, system_content: str) -> str:
        response = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},  # Гарантирует получение JSON
        )
        return response.choices[0].message.content
