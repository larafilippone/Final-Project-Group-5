import requests
from bs4 import BeautifulSoup
import re
import random
from typing import Dict, List, Optional

def get_amazon_product_data(keyword: str, search_param: str, num_pages: int=1) -> dict:
    """
    Scrapes Amazon search results for a given keyword and search parameter that is specified by the user. 

    Arguments:
    - keyword (str): The search keyword inserted by the user 
    - search_param (str): The search parameter (e.g., 'Books', 'Electronics') which is equivalent to the Amazon homepage  
    - num_pages (int): The number of pages to scrape (default is 1 to not pulling to many requests and get blocked) 

    Returns:
    - product_data (dict): A dictionary containing scraped product data with keys 'Product Name', 'Product URL', and 'ASIN'.
    """

    product_data: Dict[str, List[str]] = {'Product Name': [], 'Product URL': [], 'ASIN': []}

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

    # Randomly choose a user agent to not be blocked from scraping 

    user_agent = random.choice(user_agents)
    
    # Iterate through num_pages of the Amazon pages with the search results (using url parameter search)

    for page in range(1, num_pages + 1):
        # Using the URL with parameter search of Amazon itself 
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
        try:

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

