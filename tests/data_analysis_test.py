"""
data_analysis_test.py: This script is for testing the functions contained in data_analysis.py.
"""

import unittest
from unittest.mock import patch

from data_analysis import analyze_sentiment_with_textblob, display_wordcloud, generate_filtered_text, get_polarity_color


# Tests for analyze_sentiment_with_textblob
class TestAnalyzeSentimentWithTextblob(unittest.TestCase):
    def test_positive_sentiment(self):
        positive_text = "I really love pizza. It is amazing!"
        sentiment = analyze_sentiment_with_textblob(positive_text)
        self.assertGreater(sentiment.polarity, 0)

    def test_negative_sentiment(self):
        negative_text = "I really hate bugs. They are terrible!"
        sentiment = analyze_sentiment_with_textblob(negative_text)
        self.assertLess(sentiment.polarity, 0)

    def test_neutral_sentiment(self):
        neutral_text = "It is Monday today."
        sentiment = analyze_sentiment_with_textblob(neutral_text)
        self.assertAlmostEqual(sentiment.polarity, 0, places=1)


# Tests for get_polarity_color
class TestGetPolarityColor(unittest.TestCase):
    def test_positive_sentiment(self):
        reviews = [{"textblob_polarity": 0.5}, {"textblob_polarity": 0.6}]
        average_polarity, color = get_polarity_color(reviews)
        self.assertEqual(color, "green")
        self.assertGreater(average_polarity, 0.25)

    def test_negative_sentiment(self):
        reviews = [{"textblob_polarity": -0.5}, {"textblob_polarity": -0.6}]
        average_polarity, color = get_polarity_color(reviews)
        self.assertEqual(color, "red")
        self.assertLess(average_polarity, -0.25)

    def test_neutral_sentiment(self):
        reviews = [{"textblob_polarity": 0.2}, {"textblob_polarity": -0.1}]
        average_polarity, color = get_polarity_color(reviews)
        self.assertEqual(color, "orange")
        self.assertTrue(-0.25 <= average_polarity <= 0.25)

    def test_empty_reviews(self):
        reviews = []
        average_polarity, color = get_polarity_color(reviews)
        self.assertEqual(average_polarity, 0)
        self.assertEqual(color, "orange")  # Neutral color for no reviews

    def test_reviews_without_polarity(self):
        reviews = [{}, {}]
        average_polarity, color = get_polarity_color(reviews)
        self.assertEqual(average_polarity, 0)
        self.assertEqual(color, "orange")  # Neutral color for missing polarity


# Tests for generate_filtered_text
class TestGenerateFilteredText(unittest.TestCase):
    def test_empty_results(self):
        self.assertEqual(generate_filtered_text([]), "")

    def test_no_words_left_after_filtering(self):
        test_data = [{"review_text": "the"}]  # 'the' is a common stopword
        self.assertEqual(generate_filtered_text(test_data), "")

    def test_correct_processing(self):
        test_data = [
            {"review_text": "First review text with some words."},
            {"review_text": "Second review text, with more words!?"},
        ]
        expected_result = "First review text words Second review text words"
        self.assertEqual(generate_filtered_text(test_data), expected_result)

    def test_handling_non_alphabetic_characters(self):
        test_data = [
            {"review_text": "Review with numbers 4587634 and symbols #!@"},
            {"review_text": "Another:- review, with ; punctuations."},
        ]
        expected_result = "Review numbers symbols Another review punctuations"
        self.assertEqual(generate_filtered_text(test_data), expected_result)


# Tests for display_wordcloud
class TestDisplayWordcloud(unittest.TestCase):
    @patch("data_analysis.WordCloud")
    @patch("data_analysis.plt")
    def test_wordcloud_display(self, mock_plt, mock_wordcloud):
        test_data = [{"review_text": "Nice review text with actual words."}]
        display_wordcloud(test_data)
        mock_wordcloud.assert_called_once()
        mock_plt.imshow.assert_called()
        mock_plt.axis.assert_called_with("off")
        mock_plt.show.assert_called_once()

    @patch("data_analysis.print")
    def test_no_words_to_display(self, mock_print):
        test_data = [{"review_text": "the and in of"}]
        display_wordcloud(test_data)
        mock_print.assert_called_with("No words left after filtering for the word cloud.")


if __name__ == "__main__":
    unittest.main()
