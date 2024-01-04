import requests 
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging

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

URLS = [
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=1&sortBy=recent#reviews-filter-bar"
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=2&sortBy=recent#reviews-filter-bar",
 "https://www.amazon.com/product-reviews/B000063XH7/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=3&sortBy=recent#reviews-filter-bar",
 ]


def get_page_html(page_url: str) -> str:
    resp = requests.get(page_url, headers=headers)
    return resp.text


def get_reviews_from_html(page_html: str) -> BeautifulSoup:
    soup = BeautifulSoup(page_html, "lxml")
    reviews = soup.find_all("div", {"class": "a-section celwidget"})
    return reviews


def get_review_date(soup_object: BeautifulSoup):
    date_string = soup_object.find("span", {"class": "review-date"}).get_text()
    return date_string


def get_review_text(soup_object: BeautifulSoup) -> str:
    review_text = soup_object.find(
        "span", {"class": "a-size-base review-text review-text-content"}
    ).get_text()
    return review_text.strip()


def get_review_header(soup_object: BeautifulSoup) -> str:
    review_header = soup_object.find(
        "a",
        {
            "class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"
        },
    ).get_text()
    return review_header.strip()


def get_number_stars(soup_object: BeautifulSoup) -> str:
    stars = soup_object.find("span", {"class": "a-icon-alt"}).get_text()
    return stars.strip()


def get_product_name(soup_object: BeautifulSoup) -> str:
    product = soup_object.find(
        "a", {"class": "a-size-mini a-link-normal a-color-secondary"}
    ).get_text()
    return product.strip()


def orchestrate_data_gathering(single_review: BeautifulSoup) -> dict:
    return {
        "review_text": get_review_text(single_review),
        "review_date": get_review_date(single_review),
        "review_title": get_review_header(single_review),
        "review_stars": get_number_stars(single_review),
        "review_specifics": get_product_name(single_review),
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    all_results = []

    for u in URLS:
        logging.info(u)
        html = get_page_html(u)
        reviews = get_reviews_from_html(html)
        for rev in reviews:
            data = orchestrate_data_gathering(rev)
            all_results.append(data)

out = pd.DataFrame.from_records(all_results)
logging.info(f"{out.shape[0]} is the shape of the dataframe")
save_name = f"{datetime.now().strftime('%Y-%m-%d-%m')}.csv"
logging.info(f"saving to {save_name}")
#out.to_csv(save_name, sep=";", encoding='utf-8-sig')
#logging.info('Done')