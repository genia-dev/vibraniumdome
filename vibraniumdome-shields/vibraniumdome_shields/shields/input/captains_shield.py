import os
import ast
import logging
from typing import List
from uuid import UUID

import openai
from openai.error import APIConnectionError, APIError, Timeout, TryAgain
from pydantic import Json
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.model import LLMInteraction, ShieldMatch, VibraniumShield
from vibraniumdome_shields.utils import safe_loads_json


class CaptainsShieldMatch(ShieldMatch):
    llm_response: Json


class CaptainsShield(VibraniumShield):
    logger = logging.getLogger(__name__)
    _shield_name: str = "llm_shield"

    def __init__(self, openai_api_key):
        super().__init__(self._shield_name)
        if not openai_api_key:
            raise ValueError("LLMShield missed openai_api_key")
        openai.api_key = openai_api_key

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((Timeout, TryAgain, APIError, APIConnectionError)),
    )
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldMatch]:
        self.logger.info("performing scan, id='%s'", scan_id)
        llm_shield_prompt = settings["llm_shield"]["prompt"]
        llm_message = llm_interaction.get_all_user_messages()
        messages = [
            {"role": "system", "content": llm_shield_prompt},
            {"role": "user", "content": f"""<~START~>\n{llm_message}\n<~END~>"""},
        ]

        params = {
            "temperature": 0,
            "messages": messages,
            "request_timeout": 45,
        }

        if os.getenv("OPENAI_API_TYPE") == "azure":
            params["engine"] = os.getenv("OPENAI_API_DEPLOYMENT")
        else:
            params["model"] = settings.get("openai.openai_model", "gpt-3.5-turbo")

        results = []
        response = openai.ChatCompletion.create(**params)
        response_val = response["choices"][0]["message"]["content"]
        parsed_dict = safe_loads_json(response_val)
        if "true" == parsed_dict.get("eval", "true"):
            results = [CaptainsShieldMatch(llm_response=response_val, risk=1.0)]

        return results
