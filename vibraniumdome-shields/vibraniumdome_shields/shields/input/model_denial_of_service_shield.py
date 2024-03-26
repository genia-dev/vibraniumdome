import logging
import threading
from typing import Dict, List, Optional
from uuid import UUID

from pyrate_limiter import BucketFullException, Duration, InMemoryBucket, Limiter, Rate

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldDeflectionResult, VibraniumShield

from prometheus_client import Histogram

model_denial_of_service_shield_seconds_histogram = Histogram('model_denial_of_service_shield_seconds', 'Time for processing ModelDenialOfServiceShield',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

class ModelDenialOfServiceShieldDeflectionResult(ShieldDeflectionResult):
    limit_key: str  # aka user_id or ip
    identity: str  # the user_id value
    error_message: Optional[str] = None


class ModelDenialOfServiceShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.model_dos"
    _limiter_dict: Dict[str, Limiter]

    def __init__(self):
        super().__init__(self._shield_name)
        self.lock = threading.Lock()
        self._limiter_dict = {}

    def _get_limiter_key(self, llm_interaction: LLMInteraction, limit_key: str, identity: str, policy: dict):
        return llm_interaction.get_llm_app() + "__" + policy.get("id") + "__" + limit_key + "=" + identity

    def _init_limiter(self, shield_policy_config, llm_app):
        rate = Rate(shield_policy_config.get("threshold", 10), Duration.SECOND * shield_policy_config.get("interval_sec", 60))
        # map list of threshold and intervals to list of rates
        bucket = InMemoryBucket([rate])
        self._limiter_dict[llm_app] = Limiter(bucket)

    @model_denial_of_service_shield_seconds_histogram.time()
    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldDeflectionResult]:
        shield_matches = []
        limit_key = shield_policy_config.get("limit_by", "llm.user")
        if "llm.user" == limit_key:
            identity = llm_interaction.get_llm_user()
        else:
            identity = llm_interaction.get(limit_key)

        limiter_key = self._get_limiter_key(llm_interaction, limit_key, identity, policy)
        # TODO: add dictionary to get limiter by policy id (both application and tenant)
        try:
            with self.lock:
                if not self._limiter_dict.get(limiter_key):
                    self._init_limiter(shield_policy_config, limiter_key)
                try:
                    limiter = self._limiter_dict.get(limiter_key)
                    limiter.try_acquire(identity)
                    self._logger.debug("Access to critical function for %s : %s granted!", limit_key, identity)
                    shield_matches.append(ModelDenialOfServiceShieldDeflectionResult(limit_key=limit_key, identity=identity))
                except BucketFullException as err:
                    self._logger.info("Rate limit exceeded for for %s : %s", limit_key, identity)
                    shield_matches.append(
                        ModelDenialOfServiceShieldDeflectionResult(limit_key=limit_key, identity=identity, error_message=err.meta_info["error"], risk=1)
                    )
        except Exception as err:
            self._logger.exception("Failed to perform ModelDenialOfServiceShield, scan_id=%d", scan_id)
            raise err
        return shield_matches
