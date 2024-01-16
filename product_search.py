import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
import re
import random

# Dictionary mapping search_param options to corresponding categories on the Amazon website 

search_params = {
    " ": "All",
    "arts-crafts-intl-ship": "Arts & Crafts",
    "automotive-intl-ship": "Automotive",
    "baby-products-intl-ship": "Baby",
    "beauty-intl-ship": "Beauty & Personal Care",
    "stripbooks-intl-ship": "Books",
    "fashion-boys-intl-ship": "Boys' Fashion",
    "computers-intl-ship": "Computers",
    "deals-intl-ship": "Deals",
    "digital-music": "Digital Music",
    "electronics-intl-ship": "Electronics",
    "fashion-girls-intl-ship": "Girls' Fashion",
    "hpc-intl-ship": "Health & Household",
    "kitchen-intl-ship": "Home & Kitchen",
    "industrial-intl-ship": "Industrial & Scientific",
    "digital-text": "Kindle Store",
    "luggage-intl-ship": "Luggage",
    "fashion-mens-intl-ship": "Men's Fashion",
    "movies-tv-intl-ship": "Movies & TV",
    "music-intl-ship": "Movies, CDs & Vinyl",
    "pets-intl-ship": "Pet Supplies",
    "instant-video": "Prime Video",
    "software-intl-ship": "Software",
    "sporting-intl-ship": "Sports & Outdoors",
    "tools-intl-ship": "Tools & Home Improvement",
    "toys-and-games-intl-ship": "Toys & Games",
    "videogames-intl-ship": "Video Games",
    "fashion-womens-intl-ship": "Women's Fashion"
}

# Invert the search_params dictionary
inverted_search_params = {v: k for k, v in search_params.items()}


def get_amazon_product_data(keyword, search_param, num_pages=1):
    product_data = {'Product Name': [], 'Product URL': [], 'ASIN': []}

    """
    Scrapes Amazon search results for a given keyword and search parameter that is specified by the user. 

    Arguments:
    - keyword (str): The search keyword inserted by the user 
    - search_param (str): The search parameter (e.g., 'Books', 'Electronics') which is equivalent to the Amazon homepage  
    - num_pages (int): The number of pages to scrape (default is 1 to not pulling to many requests and get blocked) 

    Returns:
    - product_data (dict): A dictionary containing scraped product data with keys 'Product Name', 'Product URL', and 'ASIN'.
    """

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
    
    for page in range(1, num_pages + 1):
        base_url = f'https://www.amazon.com/s?k={keyword}&i={search_param}&page={page}'
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
        response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for product in soup.find_all('div', {'data-asin': True}):
                #product_name = product.find('span', {'class': 'a-size-medium'}) the source code is structured differently for different categories
                product_name = product.find('span', class_=re.compile('^a-size-'))
                product_url = product.find('a', {'class': 'a-link-normal'})
                if product_name and product_url:
                    product_data['Product Name'].append(product_name.text.strip())
                    product_data['Product URL'].append(f"https://www.amazon.com{product_url['href']}")
                    
                    # Extract ASIN from the URL
                    asin_match = re.search(r'/dp/(\w+)/', product_url['href'])
                    asin = asin_match.group(1) if asin_match else None
                    product_data['ASIN'].append(asin)
        else:
            print(f"Failed to retrieve data from page {page}. Status code: {response.status_code}")

    return product_data

