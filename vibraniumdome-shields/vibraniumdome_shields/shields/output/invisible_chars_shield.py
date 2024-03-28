import logging

from vibraniumdome_shields.shields.invisible_chars_shield_base import InvisibleCharactersShieldBase
from vibraniumdome_shields.shields.model import LLMInteraction

class InvisibleOutputCharactersShield(InvisibleCharactersShieldBase):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.output.invisible"

    def __init__(self):
        super().__init__(self._shield_name)

    def _get_message_to_validate(self, llm_interaction: LLMInteraction):
        return llm_interaction.get_last_assistant_message_and_function_result()
