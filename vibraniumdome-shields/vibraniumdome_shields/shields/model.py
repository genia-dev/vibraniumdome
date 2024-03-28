import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from termcolor import colored

from vibraniumdome_shields.utils import timestamp_str


class ShieldDeflectionResult(BaseModel):
    risk: float = 0


class Risk(Enum):
    HIGH = "High"
    LOW = "Low"
    NONE = "None"


class ShieldsDeflectionResult(BaseModel):
    scan_id: UUID = Field(default_factory=uuid4)
    timestamp: str = timestamp_str()
    results: Dict[str, List[ShieldDeflectionResult]] = {}
    risk: Risk = Risk.NONE
    risk_factor: float = 0
    high_risk_shields: Set[str] = set()

    def merge(this, that: BaseModel):
        this.risk_factor = max(this.risk_factor, that.risk_factor)
        this.results.update(that.results)


class LLMInteraction:
    _interaction: dict
    _messages: List
    _completion: str = ""
    _function_call_name: str
    _id: str
    _shields_result: ShieldsDeflectionResult
    _llm_user: str
    _llm_app: str

    def __init__(self, interaction: dict):
        if not interaction or not interaction["id"] or not interaction.get("llm_prompts") or not interaction.get("service.name"):
            raise ValueError("LLMInteraction missed configuration")
        self._interaction = interaction
        self._id = interaction["id"]
        self._messages = interaction.get("llm_prompts")
        self._llm_user = interaction.get("llm.user")
        self._llm_app = interaction.get("service.name")
        if interaction.get("llm_completions"):
            self._completion = interaction.get("llm_completions")[0].get("content", "")

    def set_completion(self, completion):
        self._completion = completion

    def set_function_call_name(self, name):
        self._function_call_name = name

    def get_id(self) -> str:
        return self._id

    def get_last_message(self) -> str:
        return self._messages[-1].get("content")

    def get(self, key: str, default_value: str) -> str:
        self._interaction.get(key, default_value)

    def get_llm_user(self):
        return self._llm_user or "anonymous"

    def get_llm_app(self):
        return self._llm_app

    def get_previous_function_calls(self) -> Set:
        res = set()
        for index, msg in enumerate(self._messages):
            if index <= self._max_chain_length:
                if msg["role"] == "assistant" and msg.get("function_call") is not None:
                    res.add(msg["function_call"].get("name"))
                elif msg["role"] == "function":
                    res.add(msg.get("name"))
        return res

    def get_last_concecutive_function_call(self):
        # TODO: fix
        messages_reverse = self._messages[::-1]
        list_length = len(messages_reverse)
        length = 0
        for index, msg in enumerate(messages_reverse):
            if index < list_length - 1:
                if msg["role"] == "function":
                    length += 1
                else:
                    break
        return length > 2

    def add_function_response_message(self, function_name, function_response):
        self._add_conversation_message(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            },
        )

    def _add_conversation_message(self, msg):
        if msg is not None:
            self._messages.append(msg)

    def get_last_user_message(self):
        messages_reverse = self._messages[::-1]
        res = None
        for msg in messages_reverse:
            if msg["role"] == "user":
                res = msg.get("content")
                break
        return res

    def get_chat_completion(self):
        return self._completion

    def get_last_assistant_message(self):
        if len(self._completion) > 0:
            return self._completion

        messages_reverse = self._messages[::-1]
        res = None
        for msg in messages_reverse:
            if msg["role"] == "assistant":
                res = msg.get("content")
                break
        return res

    def get_all_user_messages(self, limit: int = -1):
        user_messages = [item["content"] for item in self._messages if item["role"] == "user"]
        if limit > 0:
            user_messages = user_messages[:limit]
        return "\n".join(user_messages)

    def get_all_user_messages_or_function_results(self, limit: int = -1):
        user_messages = [item["content"] for item in self._messages if item["role"] == "user" or item["role"] == "function"]
        if limit > 0:
            user_messages = user_messages[:limit]
        return "\n".join(user_messages)

    def get_last_assistant_message_and_function_result(self):
        results = []
        if len(self._completion) > 0:
            results.append(self._completion)

        msg = self._messages[-1]
        if msg["role"] == "assistant" or msg["role"] == "function":
            results.append(msg.get("content"))
        return "\n".join(results)

    def get_last_user_message_or_function_result(self):
        res = None
        for msg in self._messages[::-1]:
            if msg["role"] == "user" or msg["role"] == "function":
                res = msg.get("content")
                break
        return res

    # def _take_k_or_less(self, messages_list, k):
    #     return messages_list[:k] if len(messages_list) >= k else messages_list

    def pretty_print_conversation(self, logger):
        if not logger.isEnabledFor(logging.DEBUG):
            return

        role_to_color = {
            "system": "light_red",
            "user": "green",
            "assistant": "light_yellow",
            "assistant_function": "light_blue",
            "function": "magenta",
        }
        formatted_messages = []
        for message in self._messages:
            if message["role"] == "assistant" and message.get("function_call"):
                formatted_messages.append(colored(message, role_to_color["assistant_function"]))
            else:
                formatted_messages.append(colored(message, role_to_color[message["role"]]))

        formatted_messages.append(colored("list of functions:", "light_cyan"))
        logger.debug("\n".join(formatted_messages))


class VibraniumShield(ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        pass
