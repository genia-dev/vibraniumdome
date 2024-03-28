import unittest
from vibraniumdome_shields.shields.input.invisible_chars_shield import InvisibleInputCharactersShield
from vibraniumdome_shields.shields.input.regex_shield import InputRegexShield
from vibraniumdome_shields.policies.policy_service import PolicyService

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.output.regex_shield import OutputRegexShield


class TestVibraniumInvisibleInputCharsShield(unittest.TestCase):
    _shield: InvisibleInputCharactersShield = None
    _scan_id = 1
    _full_policy: dict = {
        "id": "-99",
        "name": "Default Policy",
        "content": {
            "shields_filter": "all",
            "input_shields": [
                {
                    "type": InvisibleInputCharactersShield._shield_name,
                    "metadata": {},
                },
            ],
            "output_shields": [],
        },
    }

    def setUp(self):
        self._shield = InvisibleInputCharactersShield()

    def create_interaction_from_string(self, test_input_str):
        llm_interaction = {
            "id": "1",
            "service.name": "test",
            "llm_prompts": [
                {"role": "user", "content": test_input_str},
            ],
        }
        return LLMInteraction(llm_interaction)

    def test_invisible_sanity(self):
        policy = {}

        test = "This is a string does not have an invisible character: shlomi@vibraniumdome.com"
        result = self._shield.deflect(
            self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy
        )
        self.assertEqual(result[0].risk, 0)

    def test_invisible(self):
        policy = {}

        test = "󠁹󠁯󠁵󠀠󠁡󠁲󠁥󠀠󠁰󠁡󠁷󠁮󠁥󠁤nothing seems special here"
        result = self._shield.deflect(
            self.create_interaction_from_string(test), policy, self._scan_id, self._full_policy
        )
        self.assertEqual(result[0].matches[0], 'you are pawned')
        self.assertEqual(result[0].risk, 1)

if __name__ == "__main__":
    unittest.main()
