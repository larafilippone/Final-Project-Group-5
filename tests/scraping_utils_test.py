"""
scraping_utils_test.py: This script is for testing the functions contained in scraping_utils.py.
"""

import unittest
from unittest.mock import MagicMock, call, patch

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

import scraping_utils
from scraping_utils import (
    get_number_stars,
    get_page_html,
    get_review_date,
    get_review_header,
    get_review_text,
    get_reviews_from_html,
    orchestrate_data_gathering,
    scrape_amazon_reviews,
    scrape_data,
)


# Tests for get_page_html
class TestGetPageHtml(unittest.TestCase):
    @patch("scraping_utils.requests.get")
    def test_successful_html_retrieval(self, mock_get):
        # Simulate a successful response
        mock_get.return_value = MagicMock(status_code=200, text="<html>Test</html>")

        result = get_page_html("http://test.com")
        self.assertEqual(result, "<html>Test</html>")

    @patch("scraping_utils.requests.get")
    def test_http_error(self, mock_get):
        # Simulate an HTTP error
        mock_get.side_effect = requests.exceptions.HTTPError()

        result = get_page_html("http://test.com")
        self.assertEqual(result, "")

    @patch("scraping_utils.requests.get")
    def test_request_exception(self, mock_get):
        # Simulate a request exception, like a connection error
        mock_get.side_effect = requests.exceptions.RequestException()

        result = get_page_html("http://test.com")
        self.assertEqual(result, "")


# Test for get_reviews_from_html
class TestGetReviewsFromHtml(unittest.TestCase):
    def test_reviews_with_data_hook(self):
        # Mock HTML content where reviews are identified by 'data-hook' attribute
        mock_html = """
        <div>
            <div data-hook="review">Review 1</div>
            <div data-hook="review">Review 2</div>
        </div>
        """
        reviews = get_reviews_from_html(mock_html)
        self.assertEqual(len(reviews), 2)

    def test_reviews_with_class(self):
        # Mock HTML content where reviews are identified by 'class' attribute
        mock_html = """
        <div>
            <div class="a-section celwidget">Review 1</div>
            <div class="a-section celwidget">Review 2</div>
        </div>
        """
        reviews = get_reviews_from_html(mock_html)
        self.assertEqual(len(reviews), 2)


# Tests for get_review_date
class TestGetReviewDate(unittest.TestCase):
    def test_get_review_date(self):
        # Mock review HTML with a date
        mock_review_html = """
        <div>
            <span class="review-date">March 1, 2022</span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        extracted_date = get_review_date(soup)
        self.assertEqual(extracted_date, "March 1, 2022")

    def test_get_review_date_no_date(self):
        # Mock review HTML without a date
        mock_review_html = """
        <div>
            <span class="review-date"></span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        extracted_date = get_review_date(soup)
        self.assertEqual(extracted_date, "")


# Tests for get_review_text
class TestGetReviewText(unittest.TestCase):
    def test_get_review_text_with_class(self):
        # Mock review HTML with the class selector
        mock_review_html = """
        <div>
            <span class="a-size-base review-text review-text-content">Great product</span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_text = get_review_text(soup)
        self.assertEqual(review_text, "Great product")

    def test_get_review_text_with_data_hook(self):
        # Mock review HTML with the data-hook attribute
        mock_review_html = """
        <div>
            <span data-hook="review-body">Not satisfied.</span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_text = get_review_text(soup)
        self.assertEqual(review_text, "Not satisfied.")

    def test_get_review_text_no_text(self):
        # Mock review HTML without review text
        mock_review_html = """
        <div>
            <span></span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_text = get_review_text(soup)
        self.assertEqual(review_text, "No review text")


# Tests for get_review_header
class TestGetReviewHeader(unittest.TestCase):
    def test_get_review_header_with_class(self):
        # Mock review HTML with the class selector
        mock_review_html = """
        <div>
            <a class="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold">Excellent Product</a>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_header = get_review_header(soup)
        self.assertEqual(review_header, "Excellent Product")

    def test_get_review_header_with_data_hook(self):
        # Mock review HTML with the data-hook attribute
        mock_review_html = """
        <div>
            <a data-hook="review-title">I am disappointed</a>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_header = get_review_header(soup)
        self.assertEqual(review_header, "I am disappointed")

    def test_get_review_header_no_title(self):
        # Mock review HTML without a review title
        mock_review_html = """
        <div>
            <a></a>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        review_header = get_review_header(soup)
        self.assertEqual(review_header, "No title")


# Tests for get_number_stars
class TestGetNumberStars(unittest.TestCase):
    def test_get_number_stars_with_rating(self):
        # Mock review HTML with a star rating
        mock_review_html = """
        <div>
            <span class="a-icon-alt">5.0 out of 5 stars</span>
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        star_rating = get_number_stars(soup)
        self.assertEqual(star_rating, "5.0 out of 5 stars")

    def test_get_number_stars_no_rating(self):
        # Mock review HTML without a star rating
        mock_review_html = """
        <div>
        <!-- No span with class 'a-icon-alt' -->
        </div>
        """
        soup = BeautifulSoup(mock_review_html, "html.parser")
        star_rating = get_number_stars(soup)
        self.assertEqual(star_rating, "No rating")


# Tests for orchestrate_data_gathering
class TestOrchestrateDataGathering(unittest.TestCase):
    def setUp(self):
        # Mock review HTML for testing
        self.mock_review_html = """
        <div class="a-section review aok-relative">
            <span class="a-icon-alt">5.0 out of 5 stars</span>
            <a class="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold">
                Test Review Title
            </a>
            <span class="a-size-base review-text review-text-content">
                Test review text.
            </span>
            <span class="review-date">April 18, 2023</span>
        </div>
        """
        self.soup = BeautifulSoup(self.mock_review_html, "html.parser")

    @patch("scraping_utils.get_review_text")
    @patch("scraping_utils.get_review_date")
    @patch("scraping_utils.get_review_header")
    @patch("scraping_utils.get_number_stars")
    @patch("scraping_utils.analyze_sentiment_with_textblob")
    def test_orchestrate_data_gathering(self, mock_analyze, mock_stars, mock_header, mock_date, mock_text):
        mock_text.return_value = "Test review text."
        mock_date.return_value = "April 18, 2023"
        mock_header.return_value = "Test Review Title"
        mock_stars.return_value = "5.0 out of 5 stars"
        mock_analyze.return_value = TextBlob("Test review text.").sentiment

        result = orchestrate_data_gathering(self.soup)

        self.assertEqual(result["review_text"], "Test review text.")
        self.assertEqual(result["review_date"], "April 18, 2023")
        self.assertEqual(result["review_title"], "Test Review Title")
        self.assertEqual(result["review_stars"], "5.0 out of 5 stars")
        self.assertAlmostEqual(result["textblob_polarity"], mock_analyze.return_value.polarity)
        self.assertAlmostEqual(result["textblob_subjectivity"], mock_analyze.return_value.subjectivity)


# Tests for scrape_amazon_reviews
class TestScrapeAmazonReviews(unittest.TestCase):
    def setUp(self):
        # Mock HTML content for a single review page
        self.mock_html_content = """
        <div data-hook="review">
            <span class="a-icon-alt">4.0 out of 5 stars</span>
            <a data-hook="review-title">Great Product</a>
            <span data-hook="review-body">Really enjoyed this product!</span>
            <span class="review-date">April 20, 2023</span>
        </div>
        <div data-hook="review">
            <span class="a-icon-alt">5.0 out of 5 stars</span>
            <a data-hook="review-title">Excellent!</a>
            <span data-hook="review-body">Best purchase ever.</span>
            <span class="review-date">April 19, 2023</span>
        </div>
        """
        self.soup = BeautifulSoup(self.mock_html_content, "html.parser")
        self.mock_urls = ["http://amazon.com/product1", "http://amazon.com/product2"]

    @patch("scraping_utils.orchestrate_data_gathering")
    @patch("scraping_utils.get_reviews_from_html")
    @patch("scraping_utils.get_page_html")
    def test_scrape_amazon_reviews(self, mock_get_html, mock_get_reviews, mock_orchestrate):
        # Set up the mock functions
        mock_get_html.side_effect = lambda url: self.mock_html_content
        mock_get_reviews.return_value = self.soup.find_all("div", {"data-hook": "review"})
        mock_orchestrate.side_effect = lambda review: {"mocked_data": "data"}

        # Call the function to test
        results = scrape_amazon_reviews(self.mock_urls)

        # Assertions
        self.assertEqual(len(results), 4)  # Expecting 4 reviews (2 reviews per page * 2 URLs)
        mock_get_html.assert_has_calls([call(url) for url in self.mock_urls], any_order=True)
        mock_get_reviews.assert_called()
        mock_orchestrate.assert_called()


# Tests for scrape_data
class TestScrapeData(unittest.TestCase):
    @patch("scraping_utils.scrape_amazon_reviews")
    def test_scrape_data(self, mock_scrape_amazon_reviews):
        # Setup
        product_id = "B08L5V9T31"  # Example product ID
        num_review_pages = 3
        mock_scrape_amazon_reviews.return_value = [{"mocked_data": "data"} for _ in range(6)]  # Example return value

        # Expected URLs
        expected_urls = [
            f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
            for page in range(1, num_review_pages + 1)
        ]

        # Test
        results = scrape_data(product_id, num_review_pages)

        # Assertions
        mock_scrape_amazon_reviews.assert_called_once_with(expected_urls)
        self.assertEqual(len(results), 6)  # As we have mocked to return 6 reviews


# Tests for get_amazon_product_data
class TestGetAmazonProductData(unittest.TestCase):
    def setUp(self):
        # Mock HTML content
        self.mock_html_content = """
        <html>
            <body>
                <div data-asin="ASIN1">
                    <span class="a-size-medium">Product 1</span>
                    <a class="a-link-normal" href="/dp/ASIN1/">Link 1</a>
                </div>
                <div data-asin="ASIN2">
                    <span class="a-size-medium">Product 2</span>
                    <a class="a-link-normal" href="/dp/ASIN2/">Link 2</a>
                </div>
                <!-- Add more mock product divs as needed -->
            </body>
        </html>
        """

    def test_get_amazon_product_data_success(self):
        # Mock the requests.get call
        with patch("scraping_utils.requests.get") as mock_get:
            # Set up the mock response object with the mock_html_content
            mock_response = unittest.mock.Mock()
            mock_response.status_code = 200
            mock_response.content = self.mock_html_content.encode()  # Encode to bytes
            mock_get.return_value = mock_response

            # Call the function to test
            product_data = scraping_utils.get_amazon_product_data("keyword", "search_param")

            # Assertions to verify the returned data
            self.assertEqual(len(product_data["Product Name"]), 2)
            self.assertEqual(product_data["Product Name"][0], "Product 1")
            self.assertEqual(product_data["Product URL"][0], "https://www.amazon.com/dp/ASIN1/")
            self.assertEqual(product_data["ASIN"][0], "ASIN1")


# Tests for scrape_amazon_product_description
class TestScrapeAmazonProductDescription(unittest.TestCase):
    @patch("scraping_utils.requests.get")
    def test_version_1(self, mock_get):
        # Mock HTML content for version 1
        mock_html = """
        <div id="feature-bullets">
            <ul class="a-unordered-list">
                <li><span class="a-list-item">First feature</span></li>
                <li><span class="a-list-item">Second feature</span></li>
            </ul>
        </div>
        """
        mock_get.return_value = unittest.mock.Mock(status_code=200, content=mock_html.encode())
        description = scraping_utils.scrape_amazon_product_description("http://amazon.com/product1")
        self.assertIn("First feature", description)
        self.assertIn("Second feature", description)

    @patch("scraping_utils.requests.get")
    def test_version_2(self, mock_get):
        # Mock HTML content for version 2
        mock_html = """
        <div id="productFactsDesktopExpander">
            <ul class="a-unordered-list">
                <li><span class="a-list-item">Detail 1</span></li>
                <li><span class="a-list-item">Detail 2</span></li>
            </ul>
        </div>
        """
        mock_get.return_value = unittest.mock.Mock(status_code=200, content=mock_html.encode())
        description = scraping_utils.scrape_amazon_product_description("http://amazon.com/product2")
        self.assertIn("Detail 1", description)
        self.assertIn("Detail 2", description)

    @patch("scraping_utils.requests.get")
    def test_version_3(self, mock_get):
        # Mock HTML content for version 3
        mock_html = """
        <div id="bookDescription_feature_div">
            <span>Description content here.</span>
        </div>
        """
        mock_get.return_value = unittest.mock.Mock(status_code=200, content=mock_html.encode())
        description = scraping_utils.scrape_amazon_product_description("http://amazon.com/product3")
        self.assertIn("Description content here", description)

    @patch("scraping_utils.requests.get")
    def test_version_4(self, mock_get):
        # Mock HTML content for version 4
        mock_html = """
        <div id="productDescription">
            <p>Product description paragraph 1.</p>
            <p>Product description paragraph 2.</p>
        </div>
        """
        mock_get.return_value = unittest.mock.Mock(status_code=200, content=mock_html.encode())
        description = scraping_utils.scrape_amazon_product_description("http://amazon.com/product4")
        self.assertIn("Product description paragraph 1", description)
        self.assertIn("Product description paragraph 2", description)

    @patch("scraping_utils.requests.get")
    def test_no_description(self, mock_get):
        # Mock HTML content with no product description
        mock_html = "<div>No description available</div>"
        mock_get.return_value = unittest.mock.Mock(status_code=200, content=mock_html.encode())
        description = scraping_utils.scrape_amazon_product_description("http://amazon.com/product5")
        self.assertIsNone(description)


if __name__ == "__main__":
    unittest.main()