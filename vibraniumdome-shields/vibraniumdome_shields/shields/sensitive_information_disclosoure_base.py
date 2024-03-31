from abc import abstractmethod
import logging
from typing import List
from uuid import UUID

import spacy
from presidio_analyzer import AnalyzerEngine

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

sensitive_information_disclosoure_base_seconds_histogram = Histogram('sensitive_information_disclosoure_base_seconds', 'Time for processing SensitiveInformationDisclosureShieldBase',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class SensitiveShieldDeflectionResult(ShieldDeflectionResult):
    result: dict


class SensitiveInformationDisclosureShieldBase(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _default_entites = [
        "CREDIT_CARD",
        "PERSON",
        "URL",
        "PHONE_NUMBER",
        "IP_ADDRESS",
        "EMAIL_ADDRESS",
        "DATE_TIME",
        "LOCATION",
        "US_PASSPORT",
        "US_BANK_NUMBER",
        "US_DRIVER_LICENSE",
    ]

    def __init__(self, shield_name: str, model_name):
        super().__init__(shield_name)
        try:
            if not spacy.util.is_package(model_name):
                self._logger.info("Start spacy download")
                spacy.cli.download(model_name)
            self._logger.info("Spacy is up to date")
            self.analyzer = AnalyzerEngine()
        except Exception:
            self._logger.exception("Failed spacy download")

    @abstractmethod
    def _get_message_to_validate(self, llm_interaction: LLMInteraction) -> str:
        pass

    @sensitive_information_disclosoure_base_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        shield_matches = []
        threshold = shield_policy_config.get("threshold", 0.1)
        policy_entities = shield_policy_config.get("entities", self._default_entites)
        try:
            message: str = self._get_message_to_validate(llm_interaction)
            if message:
                analyzer_results = self.analyzer.analyze(text=message, entities=policy_entities, language="en")
                for result in analyzer_results:
                    if result.score > threshold:
                        shield_matches.append(
                            SensitiveShieldDeflectionResult(
                                risk=result.score, result={key: value for key, value in result.to_dict().items() if key != "recognition_metadata"}
                            )
                        )
        except Exception:
            self._logger.exception("Presidio Analyzer error, scan_id: %s", scan_id)

        if len(shield_matches) == 0:
            shield_matches.append(SensitiveShieldDeflectionResult(result={}))

        return shield_matches
