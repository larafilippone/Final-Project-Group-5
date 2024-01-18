import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
import re
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

def scrape_amazon_product_description(product_url):
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

    response = requests.get(product_url, headers=headers)

    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')
        no_return = True # to not try to different search patterns 
    
        if soup.find('div', {'id': 'feature-bullets'}):
            # Find all list items within the unordered list
            product_description_div = soup.find('div', {'id': 'feature-bullets'})
            
            unordered_list = product_description_div.find('ul', {'class': 'a-unordered-list'})

            if unordered_list:
                # Find all list items within the unordered list
                item_list = unordered_list.find_all('li')

                # Extract text from each list item
                description_text = '\n'.join(item.find('span', {'class': 'a-list-item'}).text.strip() for item in item_list)

                print("version 1")
                no_return = False
                return description_text

        if soup.find('div', {'class': 'a-expander-content'}) and no_return:
            product_description_div = soup.find('div', {'class': 'a-expander-content'})
    
            # Check for an unordered list
            unordered_lists = product_description_div.find_all('ul', {'class': 'a-unordered-list'})

            if unordered_lists:
                description_text = ""
                for ul in unordered_lists:
                # Find all list items within the unordered list
                    item_list = ul.find_all('li')

                    # Extract text from each list item
                    list_text = '\n'.join('/ ' + item.find('span', {'class': 'a-list-item'}).text.strip() for item in item_list)

                    # Append the list text to the overall description
                    description_text += list_text

                print("version 2")
                no_return = False
                return description_text.strip() 


        #other books
        if soup.find('div', {'id': 'bookDescription_feature_div'}) and no_return:
            book_description_div = soup.find('div', {'id': 'bookDescription_feature_div'})

            if book_description_div:
                # Find the div with data-a-expander-name 'book_description_expander'
                expander_div = book_description_div.find('div', {'data-a-expander-name': 'book_description_expander'})
    
                # Check if the expander div exists
                if expander_div:
             
                    # Find the span elements within the expander div
                    span_elements = expander_div.find_all('span')
        
                    # Iterate through the span elements and concatenate text
                    description_text = ""
                    for span_tag in span_elements:
                        
                        description_text += span_tag.get_text(separator='\n', strip=True) + '\n'

                    print('version 3')  # Strip any leading/trailing whitespace
                    no_return = False
                    return description_text.strip() 

    
        if soup.find('div', {'id': 'productDescription'}) and no_return:
            product_description_div = soup.find('div', {'id': 'productDescription'})
            # Extract text from paragraphs inside the div
            paragraphs = product_description_div.find_all('p')
            description_text = '\n'.join(paragraph.get_text(separator='\n', strip=True) for paragraph in paragraphs)
            print('version 4')
            return description_text    
        
        # try structure with productDescription 

    return None