import unittest
from vibraniumdome_shields.shields.input.regex_shield import InputRegexShield
from vibraniumdome_shields.policies.policy_service import PolicyService

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.output.regex_shield import OutputRegexShield


class TestVibraniumCanaryShield(unittest.TestCase):
    _shield: OutputRegexShield = None
    _scan_id = 1
    _full_policy: dict

    def setUp(self):
        self._shield = OutputRegexShield()
        self._full_policy = PolicyService("mock_key")._get_default_policy()

    def create_interaction_from_string(self, str):
        llm_interaction = {
            "id": "1",
            "service.name": "test",
            "llm_prompts": [
                {"role": "user", "content": "how can i get a quote for my email contact@vibraniumdome.com?"},
            ],
            "llm_completions": [{"finish_reason": "stop", "role": "assistant", "content": str}],
        }
        return LLMInteraction(llm_interaction)

    def test_no_regex(self):
        policy = {}
        test = "your secret credit card is: '5105105105105100' and email: contact@vibraniumdome.com"
        result = self._shield.deflect(self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)

    def test_non_existing_regex(self):
        policy = {"name": "founders email", "patterns": ["none@none.com"], "patterns_type": "black-list"}
        test = "your secret credit card is: '5105105105105100' and email: contact@vibraniumdome.com"
        result = self._shield.deflect(self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)

    def test_email_card(self):
        policy = {"name": "credit card and email", "patterns": ["contact@vibraniumdome.com", "5105105105105100"], "patterns_type": "black-list"}
        test = "your secret credit card is: '5105105105105100' and email: contact@vibraniumdome.com"
        result = self._shield.deflect(self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 1)
        self.assertEqual(result[1].risk, 1)

    def test_letters_only(self):
        policy = {"name": "credit card and email", "patterns": ["[a-zA-Z0-9 ]+"], "patterns_type": "white-list"}
        test = "your secret credit card is 5105105105105100 and email contact at vibraniumdome com"
        result = self._shield.deflect(self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)

    def test_letters_special_chars(self):
        policy = {"name": "credit card and email", "patterns": ["^[a-zA-Z0-9 ]+$"], "patterns_type": "white-list"}
        test = "your secret credit card is 5105105105105100 and email contact@vibraniumdome.com"
        result = self._shield.deflect(self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 1)


if __name__ == "__main__":
    unittest.main()
