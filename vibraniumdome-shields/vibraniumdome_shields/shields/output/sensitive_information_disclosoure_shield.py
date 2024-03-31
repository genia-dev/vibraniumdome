import logging

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.sensitive_information_disclosoure_base import SensitiveInformationDisclosureShieldBase


class SensitiveInformationDisclosureShieldOutput(SensitiveInformationDisclosureShieldBase):
    _logger = logging.getLogger(__name__)
    _shield_name: str = "com.vibraniumdome.shield.output.sensitive_info_disc"

    def __init__(self, model_name):
        super().__init__(self._shield_name, model_name=model_name)

    def _get_message_to_validate(self, llm_interaction: LLMInteraction) -> str:
        return llm_interaction.get_chat_completion()
