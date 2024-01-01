import unittest
from vibraniumdome_shields.shields.input.no_ip_in_urls_shield import NoIPInURLsShield
from vibraniumdome_shields.policies.policy_service import PolicyService

from vibraniumdome_shields.shields.model import LLMInteraction


class TestVibraniumBannedIpShield(unittest.TestCase):
    _shield: NoIPInURLsShield = None
    _scan_id = 1
    _full_policy: dict

    def setUp(self):
        self._shield = NoIPInURLsShield()
        self._full_policy = PolicyService("mock_key")._get_default_policy()

    def create_interaction_from_string(self, str):
        llm_interaction = {
            "id": "1",
            "service.name": "test",
            "llm_prompts": [
                {"role": "user", "content": "Hi how are you doing?"},
                {"role": "function", "content": str},
            ],
            "llm_completions": [{"finish_reason": "stop", "role": "assistant", "content": "url succeed"}],
        }
        return LLMInteraction(llm_interaction)

    def test_no_url(self):
        test = "simple summary of a website"
        result = self._shield.deflect(self.create_interaction_from_string(test), self._full_policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)
        self.assertEqual(result[0].matches, [])

    def test_simple_url(self):
        test = "summarize https://www.vibraniumdome.com/playground"
        result = self._shield.deflect(self.create_interaction_from_string(test), self._full_policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 0)
        self.assertEqual(result[0].matches, [])

    def test_forbidden_ipv4(self):
        test = "Check out this website http://192.168.1.1/42/"
        result = self._shield.deflect(self.create_interaction_from_string(test), self._full_policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 1)
        self.assertEqual(result[0].matches, ["192.168.1.1"])

    def test_forbidden_ipv6(self):
        test = "Check out this website https://[2001:0db8:0000:0000:0000:ff00:0042:8329]/42"
        result = self._shield.deflect(self.create_interaction_from_string(test), self._full_policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 1)
        self.assertEqual(result[0].matches, ["2001:0db8:0000:0000:0000:ff00:0042:8329"])

    def test_forbidden_composed(self):
        test = """
        summarize those urls':
        1. https://www.vibraniumdome.com/playground
        2. http://192.168.1.1/42
        3. http://[2001:db8::/32]/42
        """
        result = self._shield.deflect(self.create_interaction_from_string(test), self._full_policy, self._scan_id, self._full_policy)
        self.assertEqual(result[0].risk, 1)

if __name__ == "__main__":
    unittest.main()
