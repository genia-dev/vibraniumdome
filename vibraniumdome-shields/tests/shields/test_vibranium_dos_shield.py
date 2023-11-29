import unittest
from vibraniumdome_shields.shields.input.model_denial_of_service_shield import ModelDenialOfServiceShield
from vibraniumdome_shields.policies.policy_service import PolicyService

from vibraniumdome_shields.shields.model import LLMInteraction


class TestVibraniumModelDenialOfServiceShield(unittest.TestCase):
    _shield: ModelDenialOfServiceShield = None
    _scan_id = 1
    _policy: dict

    def setUp(self):
        self._shield = ModelDenialOfServiceShield()
        self._policy = PolicyService("mock_key").get_default_policy()


    def create_interaction_from_string(self, prompt: str) -> LLMInteraction:
        llm_interaction = {
            "id": "1",
            "llm.user": "shlomi",
            "service.name": "insurance_classifier_ds",
            "llm_prompts": [{"role": "user", "content": prompt}],
        }
        return LLMInteraction(llm_interaction)

    def test_sanity(self):
        interaction = self.create_interaction_from_string("hello world")
        result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)
        self.assertEqual(result, [], "The result is not an empty list")

    def test_10(self):
        interaction = self.create_interaction_from_string("hello world")
        for i in range(10):
            result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)
        self.assertEqual(result, [], "The result is not an empty list")

    def test_11(self):
        interaction = self.create_interaction_from_string("hello world")
        for i in range(11):
            result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)
        self.assertEqual(result[0].identity, "shlomi", "The identity is not the user name")

    def test_10_plus_1_app(self):
        interaction = self.create_interaction_from_string("hello world")
        for i in range(10):
            result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)

        interaction._interaction["service.name"] = interaction._llm_app = "a brand new app"
        result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)
        # different app is a diffrent limiter
        self.assertEqual(result, [], "The result is not an empty list")

    def test_10_plus_1_policy(self):
        interaction = self.create_interaction_from_string("hello world")
        for i in range(10):
            result = self._shield.deflect(interaction, self._policy["content"]["input_shields"][4]["metadata"], self._scan_id, self._policy)

        new_policy = {}
        new_policy.update(self._policy)
        new_policy["id"] = "-42"
        result = self._shield.deflect(interaction, new_policy["content"]["input_shields"][4]["metadata"], self._scan_id, new_policy)
        # new policy is a diffrent limiter
        self.assertEqual(result, [], "The result is not an empty list")


if __name__ == "__main__":
    unittest.main()
