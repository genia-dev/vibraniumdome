import logging
from typing import List
from uuid import UUID
from typing import Optional

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class CanaryTokenDisclosureShieldDeflectionResult(ShieldDeflectionResult):
    token: Optional[str] = None


class CanaryTokenDisclosureShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.output.refusal.canary_token_disc"

    def __init__(self):
        super().__init__(self._shield_name)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        shield_matches = []
        try:
            completion_message: str = llm_interaction.get_chat_completion()
            canary_tokens = shield_policy_config.get("canary_tokens", [])
            for token in canary_tokens:
                if token in completion_message:
                    self._logger.debug("token: %s appears in completion_message: %s", token, completion_message)
                    shield_matches.append(CanaryTokenDisclosureShieldDeflectionResult(name=shield_policy_config.get("name", ""), token=token, risk=1))
        except Exception:
            self._logger.exception("CanaryTokenDisclosureShield error, scan_id: %s", scan_id)
        if len(shield_matches) == 0:
            shield_matches.append(CanaryTokenDisclosureShieldDeflectionResult())
        return shield_matches
