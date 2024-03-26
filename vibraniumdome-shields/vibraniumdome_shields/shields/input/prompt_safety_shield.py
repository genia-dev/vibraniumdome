import logging
from typing import List
from uuid import UUID

import openai
from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

prompt_safety_shield_seconds_histogram = Histogram('prompt_safety_shield_seconds', 'Time for processing PromptSafetyShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class PromptSafetyShieldResult(ShieldDeflectionResult):
    category: str
    category_score: float


class PromptSafetyShield(VibraniumShield):
    """
    {
      "id": "modr-XXXXX",
      "model": "text-moderation-005",
      "results": [
        {
          "flagged": true,
          "categories": {
            "sexual": false,
            "hate": false,
            "harassment": false,
            "self-harm": false,
            "sexual/minors": false,
            "hate/threatening": false,
            "violence/graphic": false,
            "self-harm/intent": false,
            "self-harm/instructions": false,
            "harassment/threatening": true,
            "violence": true,
          },
          "category_scores": {
            "sexual": 1.2282071e-06,
            "hate": 0.010696256,
            "harassment": 0.29842457,
            "self-harm": 1.5236925e-08,
            "sexual/minors": 5.7246268e-08,
            "hate/threatening": 0.0060676364,
            "violence/graphic": 4.435014e-06,
            "self-harm/intent": 8.098441e-10,
            "self-harm/instructions": 2.8498655e-11,
            "harassment/threatening": 0.63055265,
            "violence": 0.99011886,
          }
        }
      ]
    }
    """

    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.prompt_safety"

    def __init__(self):
        super().__init__(self._shield_name)

    @prompt_safety_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        shield_matches = []

        try:
            text = llm_interaction.get_all_user_messages()
            response = openai.Moderation.create(input=text)
            result = response.results[0]
            if result["flagged"]:
                category_scores = result["category_scores"]
                shield_matches = [
                    PromptSafetyShieldResult(category=category, category_score=category_scores.get(category), risk=1)
                    for category, flag in result.get("categories").items()
                    if flag
                ]
            else:
                [PromptSafetyShieldResult(category="", category_score=0.0, risk=0)]
        except Exception:
            self._logger.exception("Safety API error")

        return shield_matches
