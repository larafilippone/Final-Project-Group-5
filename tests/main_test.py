"""
main_test.py: This script is for testing the functions contained in main.py. Some of the functions contained in main.py
are better tested directly in the Tkinter environment, amd are therefore not taken into account here.
"""
import threading
import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

import main
from main import start_scraping_thread


# Tests for run_scraping
class TestRunScraping(unittest.TestCase):
    def setUp(self):
        # Mock the GUI elements and global variables
        main.text_area = MagicMock()
        main.scrape_button = MagicMock()
        main.review_pages_entry = MagicMock()
        main.product_id = None
        main.all_results = []

    @patch("main.scrape_data")
    @patch("main.is_valid_asin", return_value=True)
    @patch("main.display_review")
    @patch("main.display_average_polarity_and_color")
    @patch("main.display_chatgpt")
    def test_run_scraping_valid_product(
        self,
        mock_display_chatgpt,
        mock_display_average_polarity_and_color,
        mock_display_review,
        mock_is_valid_asin,
        mock_scrape_data,
    ):
        # Set up for a valid product ID and review pages
        main.product_id = "valid_id"
        main.review_pages_entry.get.return_value = "2"
        mock_scrape_data.return_value = [{"review_title": "Sample Title", "review_text": "Sample Review Text"}]

        # Run the function
        main.run_scraping()

        # Assertions
        mock_display_review.assert_called()
        mock_scrape_data.assert_called_with("valid_id", 2)
        mock_display_average_polarity_and_color.assert_called()
        mock_display_chatgpt.assert_called()

    @patch("main.scrape_data")
    @patch("main.is_valid_asin", return_value=False)
    def test_run_scraping_invalid_product_id(self, mock_is_valid_asin, mock_scrape_data):
        # Set up for an invalid product ID
        main.product_id = "invalid_id"
        main.review_pages_entry.get.return_value = "2"

        # Run the function
        main.run_scraping()

        # Assertions
        main.text_area.insert.assert_called_with(tk.INSERT, "Please enter a valid product ID.\n")
        mock_scrape_data.assert_not_called()

    @patch("main.scrape_data")
    @patch("main.is_valid_asin", return_value=True)
    def test_run_scraping_invalid_review_pages(self, mock_is_valid_asin, mock_scrape_data):
        # Set up for a valid product ID but invalid review pages
        main.product_id = "valid_id"
        main.review_pages_entry.get.return_value = "invalid"

        # Run the function
        main.run_scraping()

        # Assertions
        main.text_area.insert.assert_called_with(tk.INSERT, "Please enter a valid number of review pages.\n")
        mock_scrape_data.assert_not_called()


# Tests for start_scraping_thread
class TestStartScrapingThread(unittest.TestCase):
    @patch("main.run_scraping")
    def test_start_scraping_thread(self, mock_run_scraping):
        # Call the function
        start_scraping_thread()

        # Check if the run_scraping function is called within a thread
        self.assertTrue(
            any(isinstance(thread, threading.Thread) and thread.is_alive() for thread in threading.enumerate())
        )
        mock_run_scraping.assert_called()


if __name__ == "__main__":
    unittest.main()
