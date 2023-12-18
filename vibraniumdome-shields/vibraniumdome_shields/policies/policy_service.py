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

    def _get_default_policy(self):
        return {
            "id": "-99",
            "name": "Default Policy",
            "content": {
                "shields_filter": "all",
                "high_risk_threshold": 0.8,
                "low_risk_threshold": 0.2,
                "input_shields": [
                    {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.regexv", "metadata": {}, "name": "policy number"},
                    {"type": "com.vibraniumdome.shield.input.captain", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
                    {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.model_dos", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}},
                ],
                "output_shields": [
                    {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "name": "credit card"},
                    {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": {"canary_tokens": []}},
                    {"type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}},
                ],
            },
        }

    def get_policy_by_name(self, llm_app_name) -> dict:
        encoded_input_json = quote(json.dumps({"0": {"json": {"llmAppName": llm_app_name}}}))
        full_url = f"{self._vibranium_dome_base_url}/api/trpc/policies?batch=1&input={encoded_input_json}"
        headers = {"Authorization": f"Bearer {self._vibranium_dome_api_key}"}
        result = None
        try:
            response = requests.get(full_url, headers=headers)
            if response.ok:
                response_data = response.json()
                json_content = response_data[0]["result"]["data"]["json"]
                self._logger.info("policy: %s", json_content)
                result = json_content
        except Exception:
            self._logger.exception("failed loading policy %s", llm_app_name)
            # TODO: replace the default policy with a local cache copy mechanism
            result = self._get_default_policy()

        return result
