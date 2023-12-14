from abc import abstractmethod
import logging
import os
import re
from typing import List
from uuid import UUID

import yaml

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield
from vibraniumdome_shields.utils import load_vibranium_home


class RegexShieldDeflectionResult(ShieldDeflectionResult):
    pattern: str
    matches: List = []


class RegexShieldBase(VibraniumShield):
    logger = logging.getLogger(__name__)
    _compiled_patterns: list

    def __init__(self, shield_name: str):
        super().__init__(shield_name)
        self._compiled_patterns = []
        full_path = os.path.join(load_vibranium_home(), "vibraniumdome_shields", "vibranium-sensetive.yaml")

        data = {}
        with open(full_path, "r") as f:
            data = yaml.safe_load(f)

        for pattern in data.get("patterns"):
            self._compiled_patterns.append(re.compile(pattern))

    @abstractmethod
    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        pass

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        llm_message = self._get_message_to_validate(llm_interaction)
        shield_matches = []

        # vibranium dome configured regex
        for compiled_pattern in self._compiled_patterns:
            try:
                matches = compiled_pattern.findall(llm_message)
                if matches:
                    regex_shield_match = RegexShieldDeflectionResult(name="vibranium-sensetive", pattern=compiled_pattern, matches=matches, risk=1)
                    shield_matches.append(regex_shield_match)
            except Exception:
                self.logger.exception("Failed to evaluate regex pattern %s", compiled_pattern)

        # policy configured regex
        if shield_policy_config.get("patterns"):
            for pattern in shield_policy_config.get("patterns"):
                try:
                    matches = re.compile(pattern).findall(llm_message)
                    if matches:
                        regex_shield_match = RegexShieldDeflectionResult(name=shield_policy_config.get("name", ""), pattern=pattern, matches=matches, risk=1)
                        shield_matches.append(regex_shield_match)
                except Exception:
                    self.logger.exception("Failed to evaluate regex pattern %s", pattern)

        return shield_matches
