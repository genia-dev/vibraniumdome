import logging
import unittest

from vibraniumdome_shields.shields.model import LLMInteraction


class TestVibraniumLLMInteraction(unittest.TestCase):
    _logger = logging.getLogger(__name__)

    def setUp(self):
        self._logger.info("setup")
        self._simple_user_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played shlomi@vibranium-dome.com?"},
        ]

        self._simple_assistant_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played shlomi@vibranium-dome.com?"},
            {"role": "assistant", "content": "Sorry, i can not help you with that"},
        ]

        self._another_assistant_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": "2"},
            {"role": "user", "content": "3"},
            {"role": "assistant", "content": "4"},
        ]

        self._another_user_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": "2"},
            {"role": "user", "content": "3"},
            {"role": "assistant", "content": "4"},
            {"role": "user", "content": "5"},
        ]

        self.function_call_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "NY"}}},
        ]

        self.function_call_response_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "NY"}}},
            {"role": "function", "name": "get_current_weather", "content": {"temp": 20, "units": "celsius"}},
        ]

        self.consecutive_function_call_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "NY"}}},
            {"role": "function", "name": "get_current_weather", "content": '{"temp": 20, "units": "celsius"}'},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "LA"}}},
        ]

        self.consecutive_function_call_response_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "1"},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "NY"}}},
            {"role": "function", "name": "get_current_weather", "content": '{"temp": 20, "units": "celsius"}'},
            {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": {"location": "LA"}}},
            {"role": "function", "name": "get_current_weather", "content": '{"temp": 30, "units": "celsius"}'},
        ]

    def test_last_message(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._simple_user_message})
        self.assertEqual(interaction.get_last_message(), "Where was it played shlomi@vibranium-dome.com?")

    def test_last_assistant_message(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._simple_assistant_message})
        self.assertEqual(interaction.get_last_message(), "Sorry, i can not help you with that")

    def test_last_assistant_message_1(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._another_assistant_message})
        self.assertEqual(interaction.get_last_user_message(), "3")

    def test_last_assistant_message_2(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._another_assistant_message})
        self.assertEqual(interaction.get_last_assistant_message(), "4")

    def test_last_user_message(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._another_user_message})
        self.assertEqual(interaction.get_last_assistant_message(), "4")

    def test_last_user_message_1(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._another_user_message})
        self.assertEqual(interaction.get_last_user_message(), "5")

    def test_last_user_message_or_function_result(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self.consecutive_function_call_response_message})
        self.assertEqual(interaction.get_last_user_message_or_function_result(), '{"temp": 30, "units": "celsius"}')

    def test_last_user_message_or_function_result1(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self.consecutive_function_call_message})
        self.assertEqual(interaction.get_last_user_message_or_function_result(), '{"temp": 20, "units": "celsius"}')

    def test_last_user_message_or_function_result2(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self.function_call_message})
        self.assertEqual(interaction.get_last_user_message_or_function_result(), "1")

    def test_last_user_message_or_function_result3(self):
        interaction = LLMInteraction({"id": "1", "service.name": "test", "llm_prompts": self._another_user_message})
        self.assertEqual(interaction.get_last_user_message_or_function_result(), "5")


if __name__ == "__main__":
    unittest.main()
