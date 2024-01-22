"""
scraping_utils_test.py: This script is for testing the functions contained in scraping_utils.py.
"""
import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
import requests

from scraping_utils import get_page_html, get_reviews_from_html

# Tests for get_page_html
class TestGetPageHtml(unittest.TestCase):

    @patch('scraping_utils.requests.get')
    def test_successful_html_retrieval(self, mock_get):
        # Simulate a successful response
        mock_get.return_value = MagicMock(status_code=200, text="<html>Test</html>")
        
        result = get_page_html("http://test.com")
        self.assertEqual(result, "<html>Test</html>")

    @patch('scraping_utils.requests.get')
    def test_http_error(self, mock_get):
        # Simulate an HTTP error
        mock_get.side_effect = requests.exceptions.HTTPError()

        result = get_page_html("http://test.com")
        self.assertEqual(result, "")

    @patch('scraping_utils.requests.get')
    def test_request_exception(self, mock_get):
        # Simulate a request exception, like a connection error
        mock_get.side_effect = requests.exceptions.RequestException()

        result = get_page_html("http://test.com")
        self.assertEqual(result, "")

# Test for get_reviews_from_html
class TestGetReviewsFromHtml(unittest.TestCase):

    def test_reviews_with_data_hook(self):
        # Mock HTML content where reviews are identified by 'data-hook' attribute
        mock_html = '''
        <div>
            <div data-hook="review">Review 1</div>
            <div data-hook="review">Review 2</div>
        </div>
        '''
        reviews = get_reviews_from_html(mock_html)
        self.assertEqual(len(reviews), 2)

    def test_reviews_with_class(self):
        # Mock HTML content where reviews are identified by 'class' attribute
        mock_html = '''
        <div>
            <div class="a-section celwidget">Review 1</div>
            <div class="a-section celwidget">Review 2</div>
        </div>
        '''
        reviews = get_reviews_from_html(mock_html)
        self.assertEqual(len(reviews), 2)
        
# Tests for get_review_date

# Tests for get_review_text

# Tests for get_review_header

# Tests for get_number_stars

# Tests for orchestrate_data_gathering

# Tests for scrape_amazon_reviews

# Tests for scrape_data

# Tests for get_amazon_product_data

# Tests for scrape_amazon_product_description
        
if __name__ == '__main__':
    unittest.main()