import requests 
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from textblob import TextBlob
import random

# List of user agents to choose from
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 YaBrowser/21.6.0.616 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/76.0.4017.177",
]

# Randomly choose a user agent
random_user_agent = random.choice(user_agents)

# Headers used for making HTTP requests to simulate a browser visit
headers = {
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}

# URLS list for testing (can be removed if URLs are dynamically generated in the GUI script)
URLS = [
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=1&sortBy=recent#reviews-filter-bar"
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=2&sortBy=recent#reviews-filter-bar",
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=3&sortBy=recent#reviews-filter-bar",
 ]


def get_page_html(page_url: str) -> str:
    """
    Makes a request to a given URL and returns the HTML content of the page.
    Randomly selects a user agent for each request.

    Arguments:
    page_url (str): the URL of the page to scrape.

    Returns:
    str: the HTML content of the page, or an empty string if an error occurs.
    """
    try:
        # Choose a random user agent
        user_agent = random.choice(user_agents)
        headers = {
            "authority": "www.amazon.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-dest": "document",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

        response = requests.get(page_url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return ""  # Return empty string in case of an error


def get_reviews_from_html(page_html: str) -> list:
    """
    Parses HTML content and extracts review elements.

    Arguments:
    page_html (str): HTML content of a product review page.

    Returns:
    list: a collection of review elements.
    """
    soup = BeautifulSoup(page_html, "lxml")

    # Try the first class
    reviews = soup.find_all("div", class_="a-section celwidget")
    
    # If no reviews are found with the first class, try this different class
    if not reviews:
        reviews = soup.find_all("div", class_="a-section review aok-relative")
    
    return reviews


def get_review_date(soup_object: BeautifulSoup) -> str:
    """
    Extracts the review date from a BeautifulSoup object representing a single review.

    Arguments:
    soup_object (BeautifulSoup): a BeautifulSoup object representing a single review.

    Returns:
    str: the date of the review as a string.
    """
    date_string = soup_object.find("span", {"class": "review-date"}).get_text()
    return date_string


def get_review_text(soup_object: BeautifulSoup) -> str:
    """
    Extracts the review text from a BeautifulSoup object representing a single review.

    Arguments:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the text of the review.
    """
    review_text = soup_object.find(
        "span", {"class": "a-size-base review-text review-text-content"}
    ).get_text()
    return review_text.strip()

def get_review_header(soup_object: BeautifulSoup) -> str:
    """
    Extracts the review title (header) from a BeautifulSoup object representing a single review.

    Args:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the header or title of the review.
    """
    review_header = soup_object.find(
        "a", {"class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"}
    ).get_text()
    return review_header.strip()

def get_number_stars(soup_object: BeautifulSoup) -> str:
    """
    Extracts the number of stars (rating) given in a single review.

    Args:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the star rating of the review.
    """
    stars = soup_object.find("span", {"class": "a-icon-alt"}).get_text()
    return stars.strip()

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

def orchestrate_data_gathering(single_review: BeautifulSoup) -> dict:
    """
    Orchestrates the extraction of data from a single review and performs sentiment analysis.

    Args:
    single_review (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    dict: a dictionary containing extracted data and sentiment analysis of the review.
    """
    review_text = get_review_text(single_review)
    textblob_sentiment = analyze_sentiment_with_textblob(review_text)

    return {
        "review_text": review_text,
        "review_date": get_review_date(single_review),
        "review_title": get_review_header(single_review),
        "review_stars": get_number_stars(single_review),
        "textblob_polarity": textblob_sentiment.polarity,
        "textblob_subjectivity": textblob_sentiment.subjectivity
    }

def scrape_amazon_reviews(urls: list) -> list:
    """
    Scrapes Amazon reviews from a list of given URLs.

    Args:
    urls (list): a list of URLs to scrape for reviews.

    Returns:
    list: a list of dictionaries, each containing data about a review.
    """
    all_results = []
    for u in urls:
        logging.info(u)
        html = get_page_html(u)
        reviews = get_reviews_from_html(html)
        for rev in reviews:
            data = orchestrate_data_gathering(rev)
            all_results.append(data)
    return all_results

if __name__ == '__main__':
    # Main execution block for standalone testing of the script.
    # Sets up logging to report information during the execution.
    logging.basicConfig(level=logging.INFO)

    # List to store all the results from the scraping.
    all_results = []

    # Loop through each URL in the URLS list and perform the scraping.
    for u in URLS:
        logging.info(f"Scraping URL: {u}")
        html = get_page_html(u)
        reviews = get_reviews_from_html(html)

        # Extract data from each review and append to the results list.
        for rev in reviews:
            data = orchestrate_data_gathering(rev)
            all_results.append(data)

    # Convert the scraped data into a pandas DataFrame for easier handling.
    out = pd.DataFrame.from_records(all_results)
    logging.info(f"Total reviews scraped: {out.shape[0]}")

    # Construct a filename with the current datetime and save the DataFrame to a CSV file.
    save_name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    logging.info(f"Saving data to {save_name}")
    # Uncomment the below line to enable saving to CSV.
    # out.to_csv(save_name, sep=";", encoding='utf-8-sig')
    # logging.info('Data saved successfully.')

    # Print the first few rows of the DataFrame for a quick preview.
    print(out.head())