from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from openai import OpenAI, BaseModel


class LlmProviders(Enum):
    OPENAI = 'openai'
    ASYNC_OPENAI = 'async-openai'


@dataclass
class TokenUsage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


@dataclass
class LlmChatCompletionResponse:
    dict_response: dict[str, Any]
    usage: TokenUsage


class LlmProvider(ABC):
    @abstractmethod
    def get_chat_completion(
        self,
        messages: list[dict],
        response_format: BaseModel = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[list[str]] = None
    ) -> LlmChatCompletionResponse:
        pass


class OpenAIProvider(LlmProvider):
    def __init__(self, api_key: str, model: str):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def get_chat_completion(
        self,
        messages: list[dict],
        response_format: BaseModel = None,
        **kwargs,
    ) -> LlmChatCompletionResponse:
        params = {
            "model": self.model,
            "messages": messages,
            "response_format": response_format
        }

        for key, value in kwargs.items():
            if value is not None:
                params[key] = value

        response = self.client.beta.chat.completions.parse(**params)

        return LlmChatCompletionResponse(
            dict_response=response.choices[0].message.parsed,
            usage=TokenUsage(
                completion_tokens=response.usage.completion_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            )
        )
