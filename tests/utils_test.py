"""
utils_test.py: This script is for testing the functions contained in utils.py.
"""

import unittest
from unittest.mock import patch

from config import SEARCH_PARAMS
from utils import is_valid_asin, open_amazon, value_to_key


# Tests for is_valid_asin
class TestIsValidAsin(unittest.TestCase):
    def test_valid_asin(self):
        # Test a valid ASIN
        self.assertTrue(is_valid_asin("B08KHFJKZK"))

    def test_invalid_asin_length(self):
        # Test an ASIN with incorrect length
        self.assertFalse(is_valid_asin("B08KHFJ"))

    def test_invalid_asin_characters(self):
        # Test an ASIN with invalid characters
        self.assertFalse(is_valid_asin("B08KHFJ$%K"))

    def test_empty_asin(self):
        # Test an empty ASIN string
        self.assertFalse(is_valid_asin(""))


# Tests for open_amazon
class TestOpenAmazon(unittest.TestCase):
    @patch("utils.webbrowser")
    def test_open_amazon(self, mock_webbrowser):
        # Test opening a valid Amazon URL
        url = "https://www.amazon.com/dp/B08KHFJKZK"
        open_amazon(url)
        mock_webbrowser.open_new.assert_called_with(url)

    @patch("utils.webbrowser")
    def test_open_amazon_invalid_url(self, mock_webbrowser):
        # Test opening an invalid URL
        url = "not a valid url"
        open_amazon(url)
        mock_webbrowser.open_new.assert_called_with(url)


# Tests for value_to_key
class TestValueToKey(unittest.TestCase):
    def setUp(self):
        self.search_params = SEARCH_PARAMS

    def test_value_to_key_success(self):
        # Test with a value that should be in SEARCH_PARAMS
        for key, value in self.search_params.items():
            self.assertEqual(value_to_key(value), key)

    def test_value_to_key_failure(self):
        # Test with a value that should not be in SEARCH_PARAMS
        non_existing_value = "non_existing_value"
        self.assertIsNone(value_to_key(non_existing_value))


if __name__ == "__main__":
    unittest.main()
