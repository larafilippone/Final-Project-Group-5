import requests
from bs4 import BeautifulSoup
import random
from typing import Optional

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

random_user_agent = random.choice(user_agents)

def scrape_amazon_product_description(product_url: str) -> Optional[str]:
   
    """
    Function scrapes the product url to retrieve the product description. The html pages of Amazon categories are very differently structured.
    Therefore 4 different versions need to be covered. 

    Arguments:
    product_url (str): the URL of the Amazon product page 

    Returns:
    description_text (str): a string containing the product description 
    """
   
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

    # Error handling for the html request (if no connection or other problem)
    try:

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