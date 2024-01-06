from scraping import scrape_amazon_reviews
import tkinter as tk
from tkinter import scrolledtext
import threading

def run_scraping():
    """
    Retrieves and displays Amazon product reviews based on the entered product ID. The display includes the review's title,
    rating, date, product specifics, sentiment analysis scores (polarity and subjectivity), and the review text itself.

    Arguments:
    None: this function is intended to be called by a GUI event and does not take explicit arguments.

    Returns:
    None: this function does not return a value but updates the GUI directly.
    """
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

    # Display the first 5 reviews in the GUI
    for review in all_results[:5]:  
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
    """
    Starts a new thread to run the scraping process with the 'run_scraping' function.

    Arguments:
    None: this function does not take any explicit arguments.

    Returns:
    None: this function does not return a value. It starts a new thread for the scraping process.
    """
    scraping_thread = threading.Thread(target=run_scraping)
    scraping_thread.start()

# Initialize the main application window using Tkinter
app = tk.Tk()
app.title("Amazon Review Scraper")  

# Create and pack a label widget into the window, prompting for the Amazon product ID
label = tk.Label(app, text="Enter Amazon Product ID:")
label.pack()  

# Create and pack an entry widget for user input (to enter the product ID)
entry = tk.Entry(app)
entry.pack()  

# Create a button that, when clicked, will start the scraping process (it is linked to the 'start_scraping_thread' function)
scrape_button = tk.Button(app, text="Scrape Reviews", command=start_scraping_thread)
scrape_button.pack()  

# Create a scrolled text area where the scraped review data will be displayed
text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=40)
text_area.pack()  

# Start the application's main event loop, ready for user interaction
app.mainloop()