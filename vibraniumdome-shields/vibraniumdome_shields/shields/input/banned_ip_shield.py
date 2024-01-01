import logging
import re
import urllib.parse
import ipaddress
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class BannedIpDeflectionResult(ShieldDeflectionResult):
    matches: List = []

class BannedIpShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.banned_ip"
    _url_pattern = r'https?://[^\s]+'

    def __init__(self):
        super().__init__(self._shield_name)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[BannedIpDeflectionResult]:
        llm_message = llm_interaction.get_all_user_messages_or_function_results()
        shield_matches = []
        urls = re.findall(self._url_pattern, llm_message)
        for url in urls:
            try:
                domain = urllib.parse.urlparse(url).hostname
                if ipaddress.ip_address(domain):
                    shield_matches.append(BannedIpDeflectionResult(matches=[domain], risk=1))
            except ValueError:
                self._logger.exception("Failed to perform BannedIpShield, scan_id=%d", scan_id)
                continue
        if len(shield_matches) == 0:
            shield_matches.append(BannedIpDeflectionResult(matches=[], risk=0))
        return shield_matches
