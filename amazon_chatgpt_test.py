import requests
from bs4 import BeautifulSoup


def get_amazon_products(keyword, brand, num_pages=3):
    product_names = []

    for page in range(1, num_pages + 1):
        base_url = f'https://www.amazon.com/s?k={keyword}&brand={brand}&page={page}'
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
        response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for product in soup.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                product_names.append(product.text.strip())
        else:
            print(f"Failed to retrieve data from page {page}. Status code: {response.status_code}")

    return product_names

# Generate a list of a keyword or brand - create a UI to enter this keywords and generate a nice graphical representation etc.
keyword = 'bosch'
brand = 'BOSCH'
num_pages = 3  # How to scrape all?

product_names = get_amazon_products(keyword, brand, num_pages)

if product_names:
    print("List of products on Amazon:")
    for i, name in enumerate(product_names, start=1):
        print(f"{i}. {name}")
else:
    print("No product names retrieved.")

# CHAT GPT

import openai

def generate_summary(product_names):
    api_key = "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"
    openai.api_key = api_key

    prompt = f"Summarize the list of product names:\n{', '.join(product_names)}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return response['choices'][0]['text']

summary = generate_summary(product_names)
print(f"Generated Summary: {summary}")
