import logging
from typing import List
from uuid import UUID

from transformers import pipeline

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield


class PromptInjectionTransformerShieldDeflectionResult(ShieldDeflectionResult):
    model: str = ""
    label: str = ""
    threshold: float = 0.0


class PromptInjectionTransformerShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "transformer_shield"

    def __init__(self, model):
        super().__init__(self._shield_name)
        if not model:
            raise ValueError("TransformerShield missed configuration")
        self._model = model

        try:
            self.pipeline = pipeline("text-classification", model=self._model)
            self._logger.debug("Model loaded: %s", self._model)
        except Exception:
            self._logger.error("Failed to load model: %s", self._model)

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        # TODO: take threshold by policy, check if should be 0.9
        threshold = shield_policy_config.get("threshold", 0.98)
        shield_matches = []
        hits = []

        try:
            hits = self.pipeline(llm_interaction.get_last_user_message())
        except Exception as err:
            self._logger.exception("Pipeline error")
            raise err

        for rec in hits:
            self._logger.info(rec)
            if rec["label"] == "INJECTION":
                risk_score = rec["score"]
                self._logger.debug("Detected prompt injection; score={%s} threshold={%s} id={%s}", risk_score, threshold, scan_id)
                shield_matches.append(
                    PromptInjectionTransformerShieldDeflectionResult(model=self._model, label=rec["label"], threshold=threshold, risk=risk_score)
                )
        if len(shield_matches) == 0:
            shield_matches.append(PromptInjectionTransformerShieldDeflectionResult(model=self._model))
        return shield_matches
