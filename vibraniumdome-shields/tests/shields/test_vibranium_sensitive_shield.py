import unittest
from vibraniumdome_shields.policies.policy_service import PolicyService

from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.output.sensitive_information_disclosoure_shield import SensitiveInformationDisclosureShieldOutput
from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.sensitive_information_disclosoure_base import SensitiveShieldDeflectionResult


class TestVibraniumRefusalShieldSanity(unittest.TestCase):
    _sensitive_shield: SensitiveInformationDisclosureShieldOutput = None
    _scan_id = 1
    _policy: dict
    _full_policy: dict

    def setUp(self):
        self._sensitive_shield = SensitiveInformationDisclosureShieldOutput()
        self._policy = {}
        self._full_policy = PolicyService("mock_key").get_default_policy()

    def create_interaction_from_string(self, str):
        llm_interaction = {
            "id": "1",
            "service.name":"test",
            "llm_prompts": [{"role": "user", "content": "user question?"}],
            "llm_completions": [{"finish_reason": "stop", "role": "assistant", "content": str}],
        }
        return LLMInteraction(llm_interaction)

    def test_no_sensitive(self):
        test = "Is there anything else I can help you with?"
        result = self._sensitive_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)

    def test_sensitive_date(self):
        test = "Good morning!"
        expected = [{"entity_type": "DATE_TIME", "start": 5, "end": 12, "score": 0.85, "analysis_explanation": None}]
        result = self._sensitive_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(result, [SensitiveShieldDeflectionResult(result=expected)])

    def test_sensitive_phone_and_email(self):
        test = "My phone number is 212-555-5555 and my email is alan@turing.com"
        expected = [
            {"entity_type": "EMAIL_ADDRESS", "start": 48, "end": 63, "score": 1.0, "analysis_explanation": None},
            {"entity_type": "PHONE_NUMBER", "start": 19, "end": 31, "score": 0.75, "analysis_explanation": None},
            {"entity_type": "URL", "start": 53, "end": 63, "score": 0.5, "analysis_explanation": None},
        ]
        result = self._sensitive_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(result, [SensitiveShieldDeflectionResult(result=expected)])

    def test_sensitive_all(self):
        test = """
        Jane Doe, who lives in New York, visited [www.example.com] on January 1, 
        2023, emailed from jane.doe@example.com, called from 555-123-4567, 
        sent documents from her IP address 192.168.1.1, 
        included her US passport number 123456789, 
        her US bank account number 987654321, 
        and her US driver's license number D123-4567-8901 in the application.
        """

        expected = [
            {"entity_type": "EMAIL_ADDRESS", "start": 110, "end": 130, "score": 1.0, "analysis_explanation": None},
            {"entity_type": "IP_ADDRESS", "start": 202, "end": 213, "score": 0.95, "analysis_explanation": None},
            {"entity_type": "PERSON", "start": 9, "end": 17, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "LOCATION", "start": 32, "end": 40, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "DATE_TIME", "start": 71, "end": 80, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "DATE_TIME", "start": 91, "end": 95, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "LOCATION", "start": 237, "end": 239, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "DATE_TIME", "start": 256, "end": 265, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "LOCATION", "start": 280, "end": 282, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "LOCATION", "start": 331, "end": 333, "score": 0.85, "analysis_explanation": None},
            {"entity_type": "US_DRIVER_LICENSE", "start": 358, "end": 362, "score": 0.6499999999999999, "analysis_explanation": None},
            {"entity_type": "URL", "start": 51, "end": 66, "score": 0.5, "analysis_explanation": None},
            {"entity_type": "URL", "start": 110, "end": 117, "score": 0.5, "analysis_explanation": None},
            {"entity_type": "URL", "start": 119, "end": 130, "score": 0.5, "analysis_explanation": None},
            {"entity_type": "PHONE_NUMBER", "start": 144, "end": 156, "score": 0.4, "analysis_explanation": None},
            {"entity_type": "US_PASSPORT", "start": 256, "end": 265, "score": 0.4, "analysis_explanation": None},
            {"entity_type": "US_BANK_NUMBER", "start": 303, "end": 312, "score": 0.4, "analysis_explanation": None},
            {"entity_type": "US_BANK_NUMBER", "start": 256, "end": 265, "score": 0.05, "analysis_explanation": None},
            {"entity_type": "US_PASSPORT", "start": 303, "end": 312, "score": 0.05, "analysis_explanation": None},
            {"entity_type": "US_DRIVER_LICENSE", "start": 256, "end": 265, "score": 0.01, "analysis_explanation": None},
            {"entity_type": "US_DRIVER_LICENSE", "start": 303, "end": 312, "score": 0.01, "analysis_explanation": None},
        ]
        result = self._sensitive_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(result, [SensitiveShieldDeflectionResult(result=expected)])


if __name__ == "__main__":
    unittest.main()
