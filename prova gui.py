from scraping import scrape_amazon_reviews
import tkinter as tk
from tkinter import scrolledtext
import threading

def run_scraping():
    product_id = entry.get()
    if not product_id:
        text_area.insert(tk.INSERT, "Please enter a valid product ID.\n")
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    # Generate URLs for pages 1 to 10
    urls = [
        f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        for page in range(1, 11)
    ]

    # Call the scraping function from scraping.py
    all_results = scrape_amazon_reviews(urls)

    # Display the first 5 reviews, for example
    for review in all_results[:5]:  # Adjust the number as needed
        display_text = (
            f"Title: {review['review_title']}\n"
            f"Rating: {review['review_stars']}\n"
            f"Date: {review['review_date']}\n"
            f"Product Specifics: {review['review_specifics']}\n"
            f"Polarity: {review['textblob_polarity']:.2f}, "
            f"Subjectivity: {review['textblob_subjectivity']:.2f}\n"
            f"Review: {review['review_text']}\n"
            "---------------------------------------------\n"
        )
        text_area.insert(tk.INSERT, display_text)

def start_scraping_thread():
    scraping_thread = threading.Thread(target=run_scraping)
    scraping_thread.start()

app = tk.Tk()
app.title("Amazon Review Scraper")

label = tk.Label(app, text="Enter Amazon Product ID:")
label.pack()

entry = tk.Entry(app)
entry.pack()

scrape_button = tk.Button(app, text="Scrape Reviews", command=start_scraping_thread)
scrape_button.pack()

text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
text_area.pack()

app.mainloop()