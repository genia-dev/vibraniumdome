import logging
import re
from typing import List
from uuid import UUID
from urllib.parse import urlparse

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class WhitelistURLsShieldDeflectionResult(ShieldDeflectionResult):
    matches: List = []


class WhitelistURLsShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.whitelist_urls"
    _default_pattern = re.compile(r"(?i)\b(?:https?|ftp):\/\/[-A-Z0-9+&@#/%=~_|$?!:,.]*\b")

    def __init__(self):
        super().__init__(self._shield_name)

    def _match_policy_patterns(self, shield_policy_config, llm_message, shield_matches):
        policy_domains = shield_policy_config.get("trusted_domains", [])

        urls = self._default_pattern.findall(llm_message)
        if len(urls) > 0:
            self._logger.debug("found urls in the prompt %s", urls)
            for url in urls:
                domain = urlparse(url).netloc
                if domain not in policy_domains:
                    self._logger.debug("domain url: %s, does not exist in policy domains %s", domain, policy_domains)
                    shield_matches.append(WhitelistURLsShieldDeflectionResult(matches=[domain], risk=1))
        if len(shield_matches) == 0:
            shield_matches.append(WhitelistURLsShieldDeflectionResult(matches=urls))

    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        return llm_interaction.get_all_user_messages_or_function_results()

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        llm_message = self._get_message_to_validate(llm_interaction)
        shield_matches = []
        self._match_policy_patterns(shield_policy_config, llm_message, shield_matches)
        return shield_matches
