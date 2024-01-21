"""
scraping_utils.py: Contains functions and utilities for scraping data from Amazon.
"""

import random
import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
import pandas as pd
from textblob import TextBlob
import re
from typing import List, Dict
from config import USER_AGENTS, HEADERS

# Initialize global variables
all_results = []
product_df = pd.DataFrame()
product_id = None
product_url = ""

# Create a function to retrieve the HTML code of a web page
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
        user_agent = random.choice(USER_AGENTS)
        # Update the 'user-agent' in the HEADERS
        HEADERS['user-agent'] = user_agent

        response = requests.get(page_url, headers=HEADERS)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return ""  # Return empty string in case of an error

# Create a function to retrieve review elements from HTML code
def get_reviews_from_html(page_html: str) -> list:
    """
    Parses HTML content and extracts review elements.

    Arguments:
    page_html (str): HTML content of a product review page.

    Returns:
    list: a collection of review elements.
    """
    soup = BeautifulSoup(page_html, "lxml")

    # Try finding review elements by 'data-hook' attribute with value 'review'
    reviews = soup.find_all("div", attrs={"data-hook": "review"})
    
    # If no reviews are found with the 'data-hook' attribute, try different classes
    if not reviews:
        reviews = soup.find_all("div", class_="a-section celwidget")
        if not reviews:
            reviews = soup.find_all("div", class_="a-section review aok-relative")
    
    return reviews

# Create a function to retrieve the review date
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

# Create a function to retrieve the review text
def get_review_text(soup_object: BeautifulSoup) -> str:
    """
    Extracts the review text from a BeautifulSoup object representing a single review.

    Arguments:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the text of the review.
    """
    review_text = soup_object.find(
        "span", 
        {"class": "a-size-base review-text review-text-content"}
    )
    # If the class selector doesn't find the element, try the data-hook attribute
    if not review_text:
        review_text = soup_object.find("span", {"data-hook": "review-body"})
    
    return review_text.get_text().strip() if review_text else "No review text"

# Create a function to retrieve the review title
def get_review_header(soup_object: BeautifulSoup) -> str:
    """
    Extracts the review title (header) from a BeautifulSoup object representing a single review.

    Args:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the header or title of the review.
    """
    review_header = soup_object.find(
        "a", 
        {"class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"}
    )
    # If the class selector doesn't find the element, try the data-hook attribute
    if not review_header:
        review_header = soup_object.find("a", {"data-hook": "review-title"})
    
    return review_header.get_text().strip() if review_header else "No title"

# Create a function to retrieve the review rating
def get_number_stars(soup_object: BeautifulSoup) -> str:
    """
    Extracts the number of stars (rating) given in a single review.

    Args:
    soup_object (BeautifulSoup): a BeautifulSoup object for a single review.

    Returns:
    str: the star rating of the review.
    """
    star_element = soup_object.find("span", {"class": "a-icon-alt"})
    # If the class selector finds the element, extract text, otherwise return "No rating"
    if star_element:
        return star_element.get_text().strip()
    else:
        return "No rating"

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

# Create a function to orchestrate the data gathering process and sentiment analysis performance
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

# Create a function to scrape Amazon reviews
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

# Create a function to scrape new data from Amazon
def scrape_data(product_id: str, num_review_pages: int) -> List[Dict]:
    """
    Scrapes new data from Amazon based on the given product ID and the number of review pages.

    Arguments:
    product_id (str): Amazon product ID.
    num_review_pages (int): The number of review pages to scrape.

    Returns:
    List[Dict]: a list of dictionaries, each containing data about a review.
    """
    urls = [f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}" 
            for page in range(1, num_review_pages + 1)]
    scraped_data = scrape_amazon_reviews(urls)
    return scraped_data

# Create a function to get product data from Amazon
def get_amazon_product_data(keyword: str, search_param: str, num_pages: int=1) -> dict:
    """
    Scrapes Amazon search results for a given keyword and search parameter that is specified by the user. 

    Arguments:
    keyword (str): the search keyword inserted by the user 
    search_param (str): the search parameter (e.g., 'Books', 'Electronics') which is equivalent to the Amazon homepage  
    num_pages (int): the number of pages to scrape (default is 1 to not pulling to many requests and get blocked) 

    Returns:
    product_data (dict): a dictionary containing scraped product data with keys 'Product Name', 'Product URL', and 'ASIN'.
    """
    product_data: Dict[str, List[str]] = {'Product Name': [], 'Product URL': [], 'ASIN': []}

    # Iterate through num_pages of the Amazon pages with the search results
    for page in range(1, num_pages + 1):
        base_url = f'https://www.amazon.com/s?k={keyword}&i={search_param}&page={page}'
        
        try:
            # Randomly choose a user agent and update the headers
            user_agent = random.choice(USER_AGENTS)
            headers = {**HEADERS, "user-agent": user_agent}

            # Retrieves the html content of the base_url 
            response = requests.get(base_url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Search content between <div data-asin=.. and </div>
                products_list = soup.find_all('div', {'data-asin': True})

                if products_list:

                    for product in products_list:
                        #searches for content between <span class="a-size- (to account for medium, small etc.) and </span>
                        product_name = product.find_all('span', class_=re.compile('^a-size-'))
                
                        if product_name: 
                            # Concatenate the text from all matching span elements
                            product_name = ' '.join(span.text.strip() for span in product_name)
                            # Limits the length of the basic description to 70 letters 
                            product_name = product_name[:70]

                        # initialize product_url
                        product_url = ""
                        # search for content between <a class="a-link-normal... and </class>
                        product_url_class = product.find('a', {'class': 'a-link-normal'})
                        if product_url_class:
                            product_url = f"https://www.amazon.com{product_url_class['href']}"

                        if product_url_class:
                        # Extracts ASIN (Azamon Identification Number) from the URL
                            asin_match = re.search(r'/dp/(\w+)/', product_url_class['href'])
                            asin = asin_match.group(1) if asin_match else None

                        # only save the data to product_data if product_name, product_url and asin are complete 
                        if product_name and product_url and asin:
                            product_data['Product Name'].append(product_name)
                            product_data['Product URL'].append(product_url)
                            product_data['ASIN'].append(asin)

        except requests.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    return product_data

# Create a function to retrieve a product's description from Amazon
def scrape_amazon_product_description(product_url: str) -> Optional[str]:
    """
    Function scrapes the product url to retrieve the product description. The html pages of Amazon categories are very differently structured.
    Therefore, different versions need to be covered. 

    Arguments:
    product_url (str): the URL of the Amazon product page 

    Returns:
    description_text (str): a string containing the product description 
    """
    try:
        # Randomly choose a user agent and update the headers
        user_agent = random.choice(USER_AGENTS)
        headers = {**HEADERS, "user-agent": user_agent}

        response = requests.get(product_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Version 1 find content between <div id="feature-bullets" class="a-section a-spacing-medium a-spacing-top-small"> and </div>
            product_description_div = soup.find('div', {'id': 'feature-bullets'})
            if product_description_div:

                # Find the content between <ul class="a-unordered-list a-vertical a-spacing-mini"> and </ul>
                unordered_list = product_description_div.find('ul', {'class': 'a-unordered-list'})

                if unordered_list:

                    # Find all list items within the unordered list
                    item_list = unordered_list.find_all('li')

                    # Extract text from each list item
                    description_text = '\n'.join(item.find('span', {'class': 'a-list-item'}).text.strip() for item in item_list)

                    # If any problem with scraping, it can be found more easily by knowing which versions are used 
                    print("version 1")
                    
                    return description_text

            # Version 2 find content between <div id="productFactsDesktopExpander"... and </div>
            product_description_div = soup.find('div', {'id': 'productFactsDesktopExpander'})
            if product_description_div:
        
                # Check for several unordered lists betwen <ul class="a-unordered-list a-vertical a-spacing-small"> and </ul>
                unordered_lists = product_description_div.find_all('ul', {'class': 'a-unordered-list'})

                if unordered_lists:
                    description_text = ""

                    for ul in unordered_lists:
                    # Find all list items within the unordered list
                        item_list = ul.find_all('li')

                        if item_list:
                            # Extract text from each list item
                            list_text = '\n'.join('/ ' + item.find('span', {'class': 'a-list-item'}).text.strip() for item in item_list)

                            # Append the list text to the overall description
                            description_text += list_text

                    print("version 2")
                    return description_text.strip() 

            # Version 3 find content between <div id="bookDescription_feature_div"... and </div>
            product_description_div = soup.find('div', {'id': 'bookDescription_feature_div'})
            if product_description_div:

                # Find content between all <span> and </span>
                span_elements = product_description_div.find_all('span')
            
                # Iterate through the span elements and concatenate text
                if span_elements:
                    description_text = ""
                    for span_tag in span_elements:

                        description_text += span_tag.get_text(separator='\n', strip=True) + '\n'

                    print('version 3')  # Strip any leading/trailing whitespace
                    return description_text.strip() 

            # Version 4 find content between <div id="productDescription"... and </div> all at the bottom of Amazon page - the least prefered
            product_description_div = soup.find('div', {'id': 'productDescription'})
            if product_description_div:
            
                # Find content between <p> and </p>
                paragraphs = product_description_div.find_all('p')

                if paragraphs: 
                    description_text = '\n'.join(paragraph.get_text(separator='\n', strip=True) for paragraph in paragraphs)
                    print('version 4')
                    return description_text    
            
            return None

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

    # Return None if any error occurs during the scraping process
    return None