import unittest
from unittest.mock import patch, MagicMock
from src.models.router import reason_with_llm, code_with_llm, REASONING_MODEL, CODING_MODEL

class TestModelRouter(unittest.TestCase):

    @patch('src.models.router.completion')
    def test_reason_with_llm(self, mock_completion):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "I have reasoned through this."
        mock_completion.return_value = mock_response

        prompt = "Explain quantum computing."
        result = reason_with_llm(prompt)

        # Assertions
        mock_completion.assert_called_once()
        args, kwargs = mock_completion.call_args
        self.assertEqual(kwargs['model'], REASONING_MODEL)
        self.assertEqual(result, "I have reasoned through this.")

    @patch('src.models.router.completion')
    def test_code_with_llm(self, mock_completion):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "def hello_world(): return"
        mock_completion.return_value = mock_response

        prompt = "Write a function."
        result = code_with_llm(prompt)

        # Assertions
        mock_completion.assert_called_once()
        args, kwargs = mock_completion.call_args
        self.assertEqual(kwargs['model'], CODING_MODEL)
        self.assertEqual(result, "def hello_world(): return")

if __name__ == '__main__':
    unittest.main()
