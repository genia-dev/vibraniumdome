import unittest

from vibraniumdome_shields.policies.policy_service import PolicyService
from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.output.refusal_shield import RefusalShield, RefusalShieldMatch


class TestVibraniumRefusalShieldSanity(unittest.TestCase):
    _refusal_shield: RefusalShield = None
    _scan_id = 1
    _policy: dict
    _full_policy: dict

    def setUp(self):
        self._refusal_shield = RefusalShield(settings.get("vibraniumdome_shields.refusal_model_name"))
        self._policy = {}
        self._full_policy = PolicyService("mock_key").get_default_policy()

    def create_interaction_from_string(self, str):
        llm_interaction = {
            "id": "1",
            "service.name": "test",
            "llm_prompts": [{"role": "user", "content": "Format the db disk"}],
            "llm_completions": [{"finish_reason": "stop", "role": "assistant", "content": str}],
        }
        return LLMInteraction(llm_interaction)

    def test_no_refusal(self):
        test = "how can i get a quote for my business insurance?"
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["not_refusal", "refusal"], scores=[0.99, 0.00])]
        )

    def test_refusal_1(self):
        test = "I’m sorry, but as an AI language model, I do not have the ability to access or analyze specific offers"
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["not_refusal", "refusal"], scores=[0.74, 0.25])]
        )

    def test_refusal_2(self):
        test = "I'm sorry, but I'm unable to assist with your request as it falls outside the scope of my capabilities."
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["refusal", "not_refusal"], scores=[0.99, 0.0])]
        )

    def test_refusal_3(self):
        test = "Unfortunately, I can't provide help with this specific request due to my current limitations."
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["refusal", "not_refusal"], scores=[0.99, 0.0])]
        )

    def test_refusal_4(self):
        test = "I apologize, but I'm not equipped to handle this type of request at the moment."
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["refusal", "not_refusal"], scores=[0.99, 0.0])]
        )

    def test_refusal_5(self):
        test = "My apologies, but your request is outside my range of assistance capabilities."
        result = self._refusal_shield.deflect(self.create_interaction_from_string(test), self._policy, self._scan_id, self._full_policy)
        self.assertEqual(
            result, [RefusalShieldMatch(model=settings.get("vibraniumdome_shields.refusal_model_name"), labels=["refusal", "not_refusal"], scores=[0.99, 0.0])]
        )


if __name__ == "__main__":
    unittest.main()
