import logging
from typing import List
from uuid import UUID

import spacy
from presidio_analyzer import AnalyzerEngine

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldMatch, VibraniumShield


class SensitiveShieldMatch(ShieldMatch):
    result: list


class SensitiveInformationDisclosureShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "sensitive_shield"
    _entites = ["PERSON", "URL", "PHONE_NUMBER", "IP_ADDRESS", "EMAIL_ADDRESS", "DATE_TIME", "LOCATION", "US_PASSPORT", "US_BANK_NUMBER", "US_DRIVER_LICENSE"]
    _model_name: str = "en_core_web_lg"

    def __init__(self):
        super().__init__(self._shield_name)
        try:
            if not spacy.util.is_package(self._model_name):
                self._logger.info("Start spacy download")
                spacy.cli.download(self._model_name)
            self._logger.info("Spacy is up to date")
        except Exception:
            self._logger.exception("Failed spacy download")

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldMatch]:
        shield_matches = []
        try:
            # TODO: consider moving to ctor
            analyzer: AnalyzerEngine = AnalyzerEngine()
            message: str = llm_interaction.get_chat_completion()
            if message:
                result = analyzer.analyze(text=message, entities=self._entites, language="en")
                if result:
                    shield_matches.append(
                        SensitiveShieldMatch(result=[{key: value for key, value in r.to_dict().items() if key != "recognition_metadata"} for r in result])
                    )
        except Exception:
            self._logger.exception("Presidio Analyzer error, scan_id: %s", scan_id)
        return shield_matches
