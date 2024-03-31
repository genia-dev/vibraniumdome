import logging
from typing import Dict, List
from uuid import UUID
from transformers import pipeline, Pipeline
from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield
from prometheus_client import Histogram

prompt_injection_transformer_shield_seconds_histogram = Histogram('prompt_injection_transformer_shield_seconds', 'Time for processing PromptInjectionTransformerShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class PromptInjectionTransformerShieldDeflectionResult(ShieldDeflectionResult):
    model: str = ""
    label: str = ""
    threshold: float = 0.0


class PromptInjectionTransformerShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.transformer"
    _default_threshold = 0.98
    _default_model_name: str = "deepset/deberta-v3-base-injection"
    _models_dict: Dict[str, Pipeline] = {}

    def __init__(self, models_names):
        super().__init__(self._shield_name)
        if not models_names:
            raise ValueError("TransformerShield missed configuration")
        models = models_names.split(",")
        for model in models:
            self._create_model_pipeline(model)

    def _create_model_pipeline(self, model_name: str):
        try:
            if not PromptInjectionTransformerShield._models_dict.get(model_name):
                PromptInjectionTransformerShield._models_dict[model_name] = pipeline("text-classification", model=model_name)
                self._logger.debug("Model loaded: %s", model_name)
        except Exception:
            self._logger.error("Failed to load model: %s", model_name)

    def _get_model_pipeline(self, model_name: str) -> Pipeline:
        self._create_model_pipeline(model_name)
        return PromptInjectionTransformerShield._models_dict.get(model_name)

    def _safe_get_model_pipeline(self, model_name: str) -> Pipeline:
        return PromptInjectionTransformerShield._models_dict.get(model_name)

    @prompt_injection_transformer_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        # TODO: take threshold by policy, check if should be 0.9
        threshold = shield_policy_config.get("threshold", self._default_threshold)
        model_name = shield_policy_config.get("model") or PromptInjectionTransformerShield._default_model_name
        shield_matches = []
        hits = []

        try:
            hits = self._safe_get_model_pipeline(model_name)(llm_interaction.get_last_user_message_or_function_result())
        except Exception as err:
            self._logger.exception("Pipeline error")
            raise err

        for rec in hits:
            self._logger.info(rec)
            risk_score = rec["score"]
            if rec["label"] == "INJECTION" and risk_score > threshold:
                self._logger.debug("Detected prompt injection; score={%s} threshold={%s} id={%s}", risk_score, threshold, scan_id)
                shield_matches.append(
                    PromptInjectionTransformerShieldDeflectionResult(model=model_name, label=rec["label"], threshold=threshold, risk=risk_score)
                )
        if len(shield_matches) == 0:
            shield_matches.append(PromptInjectionTransformerShieldDeflectionResult(model=model_name))
        return shield_matches
