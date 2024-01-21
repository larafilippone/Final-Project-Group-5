"""
data_analysis.py: Provides functionalities for analyzing and visualizing data extracted from Amazon reviews. 
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Any
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
    total_polarity = sum(review.get('textblob_polarity', 0) for review in reviews)
    average_polarity = total_polarity / len(reviews) if reviews else 0

    # Determine the color based on average polarity
    if average_polarity < -0.25:
        color = "red"  # Red light for negative sentiment
    elif average_polarity > 0.25:
        color = "green"  # Green light for positive sentiment
    else:
        color = "orange"  # Orange light for neutral sentiment

    return average_polarity, color

# Create a function to display a word cloud
def display_wordcloud(all_results: List[Dict[str, Any]]) -> None:
    """
    Generates and displays a word cloud from the scraped reviews, excluding common stopwords.

    Arguments:
    None: this function uses global variable all_results.

    Returns:
    None: this function updates the GUI with the word cloud image.
    """
    if not all_results:
        print("No reviews to display in the word cloud.")
        return

    # NLTK Stop words
    stop_words = set(stopwords.words('english'))

    # Combine all review texts into a single string
    text = " ".join(review['review_text'] for review in all_results)

    # Tokenize the text and remove stopwords
    words = word_tokenize(text)
    filtered_text = " ".join(word for word in words if word.lower() not in stop_words and word.isalpha())

    if not filtered_text:
        print("No words left after filtering for the word cloud.")
        return

    # Generate the word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color='white').generate(filtered_text)

    # Convert to an image and display in Tkinter
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()