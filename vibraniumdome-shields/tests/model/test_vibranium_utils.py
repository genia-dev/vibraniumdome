import logging
import unittest

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.utils import safe_loads_dictionary_string


class TestVibraniumLLMInteraction(unittest.TestCase):
    _logger = logging.getLogger(__name__)

    def test_empty(self):
        parsed_dictionary = safe_loads_dictionary_string("")
        self.assertEqual(parsed_dictionary, {})

    def test_null(self):
        parsed_dictionary = safe_loads_dictionary_string()
        self.assertEqual(parsed_dictionary, {})

    def test_none(self):
        parsed_dictionary = safe_loads_dictionary_string(None)
        self.assertEqual(parsed_dictionary, {})

if __name__ == "__main__":
    unittest.main()
