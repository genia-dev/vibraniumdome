import logging
from abc import abstractmethod
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

invisible_chars_shield_base_seconds_histogram = Histogram('invisible_shield_base_seconds', 'Time for processing InvisibleCharactersShieldBase', buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class InvisibleCharactersShielDeflectionResult(ShieldDeflectionResult):
    matches: List = []

class InvisibleCharactersShieldBase(VibraniumShield):
    _logger = logging.getLogger(__name__)

    def __init__(self, shield_name: str):
        super().__init__(shield_name)

    @abstractmethod
    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        pass

    @invisible_chars_shield_base_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        invisible_chars_found = []

        for single_char in self._get_message_to_validate(llm_interaction):
            if 0xE0000 <= ord(single_char) <= 0xE007F:
                invisible_chars_found.append(chr(ord(single_char)-0xE0000))

        return [InvisibleCharactersShielDeflectionResult(matches=[''.join(invisible_chars_found)], risk=0 if len(invisible_chars_found) == 0 else 1)]
