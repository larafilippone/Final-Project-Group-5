"""
chatgpt_integration_test.py: This script is for testing the functions contained in chatgpt_integration.py.
"""

import unittest
from unittest.mock import patch

import openai

from chatgpt_integration import ask_chatgpt


class TestChatGPTIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_openai_response = {"choices": [{"message": {"content": "Test response from Chat GPT"}}]}

    # Test a successful API response.
    def test_ask_chatgpt_success(self):
        question = "What is Chat GPT?"
        with patch("openai.ChatCompletion.create", return_value=self.mock_openai_response):
            response = ask_chatgpt(question)
            self.assertEqual(response, "Test response from Chat GPT")

    # Simulate an authentication error from the API.
    def test_ask_chatgpt_authentication_error(self):
        question = "What is Chat GPT?"
        with patch("openai.ChatCompletion.create", side_effect=openai.error.AuthenticationError("Invalid API key")):
            response = ask_chatgpt(question)
            self.assertEqual(response, "Authentication error: please check your Chat GPT API key")

    # Simulate an unexpected exception.
    def test_ask_chatgpt_unexpected_error(self):
        question = "What is Chat GPT?"
        with patch("openai.ChatCompletion.create", side_effect=Exception("Unexpected error")):
            response = ask_chatgpt(question)
            self.assertEqual(response, "An unexpected error occurred while processing your request.")


if __name__ == "__main__":
    unittest.main()
