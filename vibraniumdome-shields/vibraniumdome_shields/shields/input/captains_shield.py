import os
import logging
from typing import List
from uuid import UUID

import httpx
from openai import OpenAI
from pydantic import Json

from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield
from vibraniumdome_shields.utils import safe_loads_dictionary_string

from prometheus_client import Histogram

captains_shield_seconds_histogram = Histogram('captains_shield_seconds', 'Time for processing CaptainsShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class CaptainsShieldDeflectionResult(ShieldDeflectionResult):
    llm_response: Json


class CaptainsShield(VibraniumShield):
    logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.captain"
    _openai_client: OpenAI

    def __init__(self, openai_api_key):
        super().__init__(self._shield_name)
        if not openai_api_key:
            raise ValueError("LLMShield missed openai_api_key")
        self._openai_client = OpenAI(
            api_key=openai_api_key,
            max_retries=3,
            timeout=httpx.Timeout(60.0, read=10.0, write=10.0, connect=2.0))

    @captains_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        self.logger.info("performing scan, id='%s'", scan_id)
        llm_shield_prompt = settings[self._shield_name]["prompt"]
        llm_message = llm_interaction.get_all_user_messages_or_function_results()

        params = {
            "temperature": 0,
            "messages": [
                {"role": "system", "content": llm_shield_prompt},
                {"role": "user", "content": f"""<~START~>\n{llm_message}\n<~END~>"""},
            ],
        }

        if os.getenv("OPENAI_API_TYPE") == "azure":
            params["engine"] = os.getenv("OPENAI_API_DEPLOYMENT")
        else:
            params["model"] = shield_policy_config.get("model", settings.get("openai.openai_model", "gpt-3.5-turbo"))

        results = []
        completion = self._openai_client.chat.completions.create(**params)
        response_val = completion.choices[0].message.content
        parsed_dict = safe_loads_dictionary_string(response_val)
        if "true" == parsed_dict.get("eval", "true"):
            results = [CaptainsShieldDeflectionResult(llm_response=response_val, risk=1.0)]
        else:
            results = [CaptainsShieldDeflectionResult(llm_response=response_val, risk=0)]
        return results
