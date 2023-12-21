import logging
import os
import re
from abc import abstractmethod
from typing import List
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield
from vibraniumdome_shields.utils import load_vibranium_home, safe_loads_yaml


class RegexShieldDeflectionResult(ShieldDeflectionResult):
    pattern: str
    matches: List = []


class RegexShieldBase(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _vibranium_compiled_patterns: list

    def __init__(self, shield_name: str):
        super().__init__(shield_name)
        self._vibranium_compiled_patterns = []
        full_path = os.path.join(load_vibranium_home(), "vibraniumdome_shields", "vibranium-sensetive.yaml")
        data = safe_loads_yaml(full_path)

        for pattern in data.get("patterns"):
            self._vibranium_compiled_patterns.append(re.compile(pattern))

    @abstractmethod
    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        pass

    def _match_policy_patterns(self, shield_policy_config, llm_message, shield_matches):
        policy_patterns = shield_policy_config.get("patterns", [])
        patterns_type = shield_policy_config.get("patterns_type", "black-list")
        policy_name = shield_policy_config.get("name", "")

        for pattern in policy_patterns:
            try:
                matches = re.compile(pattern).findall(llm_message)
                if matches:
                    if patterns_type == "black-list":
                        self._logger.debug("one of the black list pattern %s matches the llm message, potential risk", pattern)
                        shield_matches.append(RegexShieldDeflectionResult(name=policy_name, pattern=pattern, matches=matches, risk=1))
                    else:
                        self._logger.debug("one of the white list patterns %s matches the llm message, we are all clear", pattern)
                        shield_matches.append(RegexShieldDeflectionResult(name=policy_name, pattern=pattern, matches=matches, risk=0))
                        break
            except Exception:
                self._logger.exception("Failed to evaluate regex pattern %s", pattern)

        if len(shield_matches) == 0:
            if patterns_type == "black-list":
                self._logger.debug("None of the black list patterns matched the llm message, we are good to go")
                shield_matches.append(RegexShieldDeflectionResult(name=policy_name, pattern="any"))
            else:
                self._logger.debug("None of the white list patterns matched the policy regex, potential risk")
                shield_matches.append(RegexShieldDeflectionResult(name=policy_name, pattern="any", risk=1))

    def _match_vibraniumdome_patterns(self, llm_message, shield_matches):
        for compiled_pattern in self._vibranium_compiled_patterns:
            try:
                matches = compiled_pattern.findall(llm_message)
                if matches:
                    regex_shield_match = RegexShieldDeflectionResult(name="vibranium-sensetive", pattern=compiled_pattern, matches=matches, risk=1)
                    shield_matches.append(regex_shield_match)
            except Exception:
                self._logger.exception("Failed to evaluate regex pattern %s", compiled_pattern)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        llm_message = self._get_message_to_validate(llm_interaction)
        shield_matches = []

        self._match_vibraniumdome_patterns(llm_message, shield_matches)
        self._match_policy_patterns(shield_policy_config, llm_message, shield_matches)

        return shield_matches
