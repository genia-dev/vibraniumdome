import logging
import re
import urllib.parse
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

arbitrary_images_shield_seconds_histogram = Histogram('arbitrary_images_shield_seconds', 'Time for processing ArbitraryImagesShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class ArbitraryImagesShieldDeflectionResult(ShieldDeflectionResult):
    matches: List = []


class ArbitraryImagesShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.output.arbitrary_image"
    _default_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:png|jpg|jpeg|gif|bmp|svg)")

    def __init__(self):
        super().__init__(self._shield_name)

    def _match_policy_patterns(self, shield_policy_config, llm_message, shield_matches):
        policy_domains = shield_policy_config.get("trusted_domains", [])

        urls = self._default_pattern.findall(llm_message)
        if len(urls) > 0:
            self._logger.debug("found images in the prompt %s", urls)
            for url in urls:
                domain = urllib.parse.urlparse(url).hostname
                if domain not in policy_domains:
                    self._logger.debug("domain images: %s, does not exist in policy domains %s", domain, policy_domains)
                    shield_matches.append(ArbitraryImagesShieldDeflectionResult(matches=[domain], risk=1))
        if len(shield_matches) == 0:
            shield_matches.append(ArbitraryImagesShieldDeflectionResult(matches=urls))

    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        return llm_interaction.get_last_assistant_message_and_function_result()

    @arbitrary_images_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        llm_message = self._get_message_to_validate(llm_interaction)
        shield_matches = []
        self._match_policy_patterns(shield_policy_config, llm_message, shield_matches)
        return shield_matches
