import logging
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldMatch, VibraniumShield


class CanaryTokenDisclosureShieldMatch(ShieldMatch):
    token: str


class CanaryTokenDisclosureShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "canary_token_disclosure_shield"

    def __init__(self):
        super().__init__(self._shield_name)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldMatch]:
        shield_matches = []
        try:
            completion_message: str = llm_interaction.get_chat_completion()
            canary_tokens = shield_policy_config.get("canary_tokens", [])
            for token in canary_tokens:
                if token in completion_message:
                    self._logger.debug("token: %s appears in completion_message: %s", token, completion_message)
                    shield_matches.append(CanaryTokenDisclosureShieldMatch(name=shield_policy_config.get("name", ""), token=token, risk=1))
            return shield_matches
        except Exception:
            self._logger.exception("CanaryTokenDisclosureShield error, scan_id: %s", scan_id)
        return shield_matches
