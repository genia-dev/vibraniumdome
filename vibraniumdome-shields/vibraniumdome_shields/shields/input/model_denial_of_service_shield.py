import logging
import threading
from typing import List, Dict
from uuid import UUID

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldMatch, VibraniumShield
from pyrate_limiter import Duration, InMemoryBucket, Rate, Limiter, BucketFullException


class ModelDenialOfServiceShieldMatch(ShieldMatch):
    limit_key: str  # aka user_id or ip
    identity: str  # the user_id value


class ModelDenialOfServiceShield(VibraniumShield):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "model_denial_of_service_shield"
    _limiter_dict: Dict[str, Limiter]

    def __init__(self):
        super().__init__(self._shield_name)
        self.lock = threading.Lock()
        self._limiter_dict = {}

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldMatch]:
        shield_matches = []
        limit_key = shield_policy_config.get("limit_by", "llm.user")
        if "llm.user" == limit_key:
            identity = llm_interaction.get_llm_user()
        else:
            identity = llm_interaction.get(limit_key)

        limiter_key = self.get_limiter_key(llm_interaction, shield_policy_config, policy)
        # TODO: add dictionary to get limiter by policy id (both application and tenant)
        try:
            with self.lock:
                if not self._limiter_dict.get(limiter_key):
                    self._init_limiter(shield_policy_config, limiter_key)
                try:
                    limiter = self._limiter_dict.get(limiter_key)
                    limiter.try_acquire(identity)
                    self._logger.debug("Access to critical function for %s : %s granted!", limit_key, identity)
                except BucketFullException as err:
                    self._logger.info("Rate limit exceeded for for %s : %s", limit_key, identity)
                    shield_matches.append(ModelDenialOfServiceShieldMatch(limit_key=limit_key, identity=identity, name=err.meta_info["error"]))
        except Exception as err:
            self._logger.exception("Failed to perform ModelDenialOfServiceShield, scan_id=%d", scan_id)
            raise err
        return shield_matches

    def get_limiter_key(self, llm_interaction: LLMInteraction, shield_policy_config: dict, policy: dict):
        # app__policy__limitby
        return llm_interaction.get_llm_app() + "__" + policy.get("id") + "__" + shield_policy_config.get("limit_by")

    def _init_limiter(self, shield_policy_config, llm_app):
        rate = Rate(shield_policy_config.get("threshold", 10), Duration.SECOND * shield_policy_config.get("interval_sec", 60))
        # map list of threshold and intervals to list of rates
        bucket = InMemoryBucket([rate])
        self._limiter_dict[llm_app] = Limiter(bucket)
