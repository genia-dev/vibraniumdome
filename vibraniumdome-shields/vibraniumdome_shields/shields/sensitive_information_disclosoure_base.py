from abc import abstractmethod
import logging
from typing import List
from uuid import UUID

import spacy
from presidio_analyzer import AnalyzerEngine

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class SensitiveShieldDeflectionResult(ShieldDeflectionResult):
    result: list


class SensitiveInformationDisclosureShieldBase(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _entites = ["PERSON", "URL", "PHONE_NUMBER", "IP_ADDRESS", "EMAIL_ADDRESS", "DATE_TIME", "LOCATION", "US_PASSPORT", "US_BANK_NUMBER", "US_DRIVER_LICENSE"]
    _model_name: str = "en_core_web_lg"

    def __init__(self, shield_name: str):
        super().__init__(shield_name)
        try:
            if not spacy.util.is_package(self._model_name):
                self._logger.info("Start spacy download")
                spacy.cli.download(self._model_name)
            self._logger.info("Spacy is up to date")
        except Exception:
            self._logger.exception("Failed spacy download")

    @abstractmethod
    def _get_message_to_validate(self, llm_interaction: LLMInteraction) -> str:
        pass

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        shield_matches = []
        try:
            # TODO: consider moving to ctor
            analyzer: AnalyzerEngine = AnalyzerEngine()
            message: str = self._get_message_to_validate(llm_interaction)
            if message:
                result = analyzer.analyze(text=message, entities=self._entites, language="en")
                if result:
                    shield_matches.append(
                        SensitiveShieldDeflectionResult(result=[{key: value for key, value in r.to_dict().items() if key != "recognition_metadata"} for r in result])
                    )
        except Exception:
            self._logger.exception("Presidio Analyzer error, scan_id: %s", scan_id)
        return shield_matches
