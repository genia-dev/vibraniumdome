import ipaddress
import logging
import re
import urllib.parse
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class NoIPInURLsDeflectionResult(ShieldDeflectionResult):
    matches: List = []


class NoIPInURLsShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.no_ip_in_urls"
    _url_pattern = r"https?://[^\s]+"

    def __init__(self):
        super().__init__(self._shield_name)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[NoIPInURLsDeflectionResult]:
        llm_message = llm_interaction.get_last_assistant_message_and_function_result()
        shield_matches = []
        urls = re.findall(self._url_pattern, llm_message)
        for url in urls:
            try:
                domain = urllib.parse.urlparse(url).hostname
                if ipaddress.ip_address(domain):
                    shield_matches.append(NoIPInURLsDeflectionResult(matches=[domain], risk=1))
            except ValueError:
                continue
        if len(shield_matches) == 0:
            shield_matches.append(NoIPInURLsDeflectionResult(matches=[], risk=0))
        return shield_matches
