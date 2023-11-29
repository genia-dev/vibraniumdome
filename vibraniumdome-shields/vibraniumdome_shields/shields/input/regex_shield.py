import logging

from vibraniumdome_shields.shields.regex_shield_base import RegexShieldBase
from vibraniumdome_shields.shields.model import LLMInteraction


class InputRegexShield(RegexShieldBase):
    logger = logging.getLogger(__name__)
    _shield_name: str = "regex_shield"

    def __init__(self):
        super().__init__(self._shield_name)

    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        return llm_interaction.get_last_user_message()
