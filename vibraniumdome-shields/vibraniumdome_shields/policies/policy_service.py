import json
import logging
from urllib.parse import quote

import requests

from vibraniumdome_shields.settings_loader import settings


class PolicyService:
    _logger = logging.getLogger(__name__)
    _vibranium_dome_base_url: str
    _vibranium_dome_api_key: str

    def __init__(self, vibranium_dome_api_key: str = None):
        self._vibranium_dome_base_url = settings.get("VIBRANIUM_DOME_APP_BASE_URL", "http://localhost:3000")
        self._vibranium_dome_api_key = settings.get("VIBRANIUM_DOME_API_KEY", vibranium_dome_api_key)
        if not self._vibranium_dome_api_key:
            raise ValueError("PolicyService missed configuration 'VIBRANIUM_DOME_API_KEY'")

    def get_default_policy(self):
        return {
            "id": "-99",
            "name": "Default Policy",
            "content": {
                "shields_filter": "all",
                "high_risk_threshold": 0.8,
                "low_risk_threshold": 0.2,
                "input_shields": [
                    {"type": "vector_db_shield", "metadata": {}},
                    {"type": "regex_shield", "metadata": {}, "name": "policy number"},
                    {"type": "llm_shield", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
                    {"type": "transformer_shield", "metadata": {}},
                    {"type": "prompt_safety_shield", "metadata": {}},
                    {"type": "sensitive_shield", "metadata": {}},
                    {"type": "model_denial_of_service_shield", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}},
                ],
                "output_shields": [
                    {"type": "regex_output_shield", "metadata": {}, "name": "credit card"},
                    {"type": "refusal_shield", "metadata": {}},
                    {"type": "canary_token_disclosure_shield", "metadata": {"canary_tokens": []}},
                    {"type": "sensitive_output_shield", "metadata": {}},
                ],
            },
        }

    def get_policy_by_name(self, llm_app_name) -> dict:
        encoded_input_json = quote(json.dumps({"0": {"json": {"llmAppName": llm_app_name}}}))
        full_url = f"{self._vibranium_dome_base_url}/api/trpc/policies?batch=1&input={encoded_input_json}"
        headers = {"Authorization": f"Bearer {self._vibranium_dome_api_key}"}
        try:
            response = requests.get(full_url, headers=headers)
            if response.ok:
                response_data = response.json()
                json_content = response_data[0]["result"]["data"]["json"]
                self._logger.info("policy: %s", json_content)
                return json_content
        except Exception:
            self._logger.exception("failed loading policy %s", llm_app_name)

        return self.get_default_policy()
