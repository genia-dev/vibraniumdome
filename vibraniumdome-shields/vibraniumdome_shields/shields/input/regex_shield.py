import logging

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.regex_shield_base import RegexShieldBase


class InputRegexShield(RegexShieldBase):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.input.regex"

    def __init__(self):
        super().__init__(self._shield_name)

    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        return llm_interaction.get_last_user_message()
