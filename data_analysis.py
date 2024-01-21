"""
data_analysis.py: Provides functionalities for analyzing and visualizing data extracted from Amazon reviews. 
"""

from typing import Any, Dict, List, Tuple


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob



# Create a function to perform sentiment analysis
def analyze_sentiment_with_textblob(text: str):
    """
    Analyzes the sentiment of the given text using TextBlob.

    Args:
    text (str): the text to analyze.

    Returns:
    Sentiment: the sentiment analysis result, including polarity and subjectivity scores.
    """
    testimonial = TextBlob(text)
    return testimonial.sentiment


# Create function to calculate average polarity score and output corresponding color
def get_polarity_color(reviews: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    This function iterates through the list of reviews, sums up their polarity scores, and calculates
    the average polarity. Based on the average polarity, it assigns a color: red for negative sentiment
    (average polarity less than -0.25), green for positive sentiment (average polarity greater than 0.25),
    and orange for neutral sentiment (average polarity between -0.25 and 0.25).

    Arguments:
    reviews (List[Dict[str, Any]]): a list of dictionaries, where each dictionary represents a review
                                    and contains at least a 'textblob_polarity' key with a numeric polarity score.

    Returns:
    Tuple[float, str]: a tuple containing the average polarity as a float and the corresponding color as a string.
    """
    total_polarity = sum(review.get("textblob_polarity", 0) for review in reviews)
    average_polarity = total_polarity / len(reviews) if reviews else 0

    # Determine the color based on average polarity
    if average_polarity < -0.25:
        color = "red"  # Red light for negative sentiment
    elif average_polarity > 0.25:
        color = "green"  # Green light for positive sentiment
    else:
        color = "orange"  # Orange light for neutral sentiment

    return average_polarity, color


# Create a function to preprocess text for the word cloud
def generate_filtered_text(all_results):
    """
    Processes a collection of reviews to generate a single string of text, suitable for generating a word cloud.
    This function tokenizes the review texts, filters out common English stopwords, and concatenates the remaining words into a single string.
    Only words that are purely alphabetical are retained, so that the final string does not contain numbers or special characters.

    Arguments:
    all_results (List[Dict[str, Any]]): a list of dictionaries where each dictionary contains the data of a review.
                                        Each dictionary should have a key 'review_text' containing the text of the review.

    Returns:
    str: a single string that concatenates all the filtered words from the reviews. Returns an empty string if 'all_results' is empty or if no words are left after filtering.
    """
    if not all_results:
        return ""

    # Combine all review texts into a single string
    text = " ".join(review["review_text"] for review in all_results)

    # Tokenize the text and remove stopwords
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    return " ".join(word for word in words if word.lower() not in stop_words and word.isalpha())



