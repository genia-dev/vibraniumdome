import logging
from typing import List, Optional
from uuid import UUID
import math
from transformers import pipeline

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

refusal_shield_seconds_histogram = Histogram('refusal_shield_seconds', 'Time for processing RefusalShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class RefusalShieldDeflectionResult(ShieldDeflectionResult):
    model: Optional[str] = None
    labels: Optional[List] = None
    scores: Optional[List] = None


class RefusalShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.output.refusal"

    def __init__(self, model):
        super().__init__(self._shield_name)
        if not model:
            raise ValueError("RefusalShield missed configuration")
        self._model = model

        try:
            self.pipeline = pipeline("zero-shot-classification", model=self._model)
            self._logger.debug("Model loaded: %s", self._model)
        except Exception:
            self._logger.error("Failed to load model: %s", self._model)

    @refusal_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        threshold = shield_policy_config.get("threshold", 0.25)
        categories = ["refusal", "not_refusal"]
        shield_results = []
        result = None
        try:
            message = llm_interaction.get_chat_completion()
            if message:
                result = self.pipeline(message, categories, multi_label=False)
        except Exception as err:
            self._logger.exception("Pipeline error")
            raise err

        self._logger.debug("Model result: %s", result)
        if result:
            refusal_index = result["labels"].index("refusal")
            refusal_score = result["scores"][refusal_index]
            risk = math.floor(refusal_score * 100) / 100
            if risk >= threshold:
                shield_results.append(RefusalShieldDeflectionResult(model=self._model, labels=categories, scores=[risk, round(1 - risk, 2)], risk=risk))
            else:
                shield_results.append(RefusalShieldDeflectionResult())

        return shield_results
