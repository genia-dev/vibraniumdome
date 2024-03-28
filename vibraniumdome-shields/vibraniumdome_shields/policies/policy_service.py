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
                "redact_conversation": False,
                "input_shields": [
                    {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}, "full_name": "Prompt injection transformer shield"},
                    {
                        "type": "com.vibraniumdome.shield.input.model_dos",
                        "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"},
                        "full_name": "Model denial of service shield",
                    },
                    {
                        "type": "com.vibraniumdome.shield.input.captain",
                        "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"},
                        "full_name": "Captain's shield",
                    },
                    {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}, "full_name": "Semantic vector similarity shield"},
                    {"type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "full_name": "Regex input shield"},
                    {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}, "full_name": "Prompt safety moderation shield"},
                    {
                        "type": "com.vibraniumdome.shield.input.sensitive_info_disc",
                        "metadata": {},
                        "full_name": "PII and Sensetive information disclosure shield",
                    },
                    {"type": "com.vibraniumdome.shield.input.no_ip_in_urls", "metadata": {}, "full_name": "No IP in URLs shield"},
                    {"type": "com.vibraniumdome.shield.input.invisible", "metadata": {}, "full_name": "Invisible character input shield"},
                ],
                "output_shields": [
                    {
                        "type": "com.vibraniumdome.shield.output.refusal.canary_token_disc",
                        "metadata": {"canary_tokens": []},
                        "full_name": "Canary token disclosure shield",
                    },
                    {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}, "full_name": "Model output refusal shield"},
                    {
                        "type": "com.vibraniumdome.shield.output.sensitive_info_disc",
                        "metadata": {},
                        "full_name": "PII and sensetive information disclosure shield",
                    },
                    {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "full_name": "Regex output shield"},
                    {"type": "com.vibraniumdome.shield.output.arbitrary_image", "metadata": {}, "full_name": "Arbitrary image domain URL shield"},
                    {"type": "com.vibraniumdome.shield.output.whitelist_urls", "metadata": {}, "full_name": "White list domains URL shield"},
                    {"type": "com.vibraniumdome.shield.output.invisible", "metadata": {}, "full_name": "Invisible character input shield"},
                ],
            },
        }

    def get_base_policy(self) -> dict:
        full_url = f"{self._vibranium_dome_base_url}/api/trpc/base_policy"
        headers = {"Authorization": f"Bearer {self._vibranium_dome_api_key}"}
        try:
            response = requests.get(full_url, headers=headers)
            if response.ok:
                response_data = response.json()
                result = response_data["result"]["data"]["json"]
                self._logger.debug("policy: %s", result)
        except Exception:
            self._logger.exception("failed loading base policy")
            result = self._get_default_policy()

        return result

    def get_shields_names(self) -> dict:
        policy = self.get_base_policy()
        return dict(map(lambda item: (item['type'], item['full_name']), policy["input_shields"] + policy["output_shields"]))

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
                self._logger.debug("policy: %s", json_content)
                result = json_content
        except Exception:
            self._logger.exception("failed loading policy %s", llm_app_name)
            # TODO: replace the default policy with a local cache copy mechanism
            result = self._get_default_policy()

        return result
