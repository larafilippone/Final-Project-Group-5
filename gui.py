from scraping import scrape_amazon_reviews
import tkinter as tk
from tkinter import scrolledtext, StringVar
import threading

# Initialize all_results as an empty list.
all_results = []

def run_scraping() -> None:
    """
    Retrieves and displays Amazon product reviews based on the entered product ID. The display includes the review's title,
    rating, date, product specifics, sentiment analysis scores (polarity and subjectivity), and the review text itself.

    Arguments:
    None: this function is intended to be called by a GUI event and does not take explicit arguments.

    Returns:
    None: this function does not return a value but updates the GUI directly.
    """
    global all_results
    
    # Disable the scrape button to prevent concurrent scraping
    scrape_button.config(state=tk.DISABLED)
    
    # Clear the previous results from the text area
    text_area.delete('1.0', tk.END)

    product_id = entry.get()
    if not product_id:
        text_area.insert(tk.INSERT, "Please enter a valid product ID.\n")
        
        # Re-enable the scrape button
        scrape_button.config(state=tk.NORMAL)
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    # Generate URLs for pages 1 to 10
    urls = [
        f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        for page in range(1, 11)
    ]

    # Call the scraping function from scraping.py
    all_results = scrape_amazon_reviews(urls)

    # Display the first 10 reviews in the GUI
    for review in all_results[:10]:
        display_review(review)
    
    # Re-enable the scrape button
    scrape_button.config(state=tk.NORMAL)

    # Generate URLs for pages 1 to 10
    urls = [
        f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        for page in range(1, 11)
    ]

    # Call the scraping function from scraping.py
    all_results = scrape_amazon_reviews(urls)

    # Display the first 10 reviews in the GUI
    for review in all_results[:10]:  
        display_text = (
            f"Title: {review['review_title']}\n"
            f"Rating: {review['review_stars']}\n"
            f"Date: {review['review_date']}\n"
            f"Polarity: {review['textblob_polarity']:.2f}, "
            f"Subjectivity: {review['textblob_subjectivity']:.2f}\n"
            f"Review: {review['review_text']}\n"
            "---------------------------------------------\n"
        )
        text_area.insert(tk.INSERT, display_text)

def apply_filters() -> None:
    """
    Filters and displays reviews based on specified sentiment analysis criteria.
    The filters applied are based on minimum and maximum values for subjectivity and polarity.

    Arguments:
    None: this function relies on global variables and user input from the GUI.

    Returns:
    None: this function does not return any value but updates the GUI directly.
    """
    min_subjectivity = float(min_subjectivity_entry.get()) if min_subjectivity_entry.get() else 0.0
    max_subjectivity = float(max_subjectivity_entry.get()) if max_subjectivity_entry.get() else 1.0
    min_polarity = float(min_polarity_entry.get()) if min_polarity_entry.get() else -1.0
    max_polarity = float(max_polarity_entry.get()) if max_polarity_entry.get() else 1.0

    text_area.delete('1.0', tk.END)  # Clear the existing text

    filtered_reviews = [review for review in all_results
                        if min_subjectivity <= review['textblob_subjectivity'] <= max_subjectivity
                        and min_polarity <= review['textblob_polarity'] <= max_polarity]

    for review in filtered_reviews[:10]:  # Display 10 of the filtered reviews
        display_review(review)

def display_review(review) -> None:
    """
    Displays a single review in the text area of the GUI.

    Arguments:
    review (dict): a dictionary containing details of a single review including title,
                   rating, date, product specifics, polarity, subjectivity, and review text.

    Returns:
    None: this function does not return any value but updates the GUI directly.
    """
    display_text = (
        f"Title: {review['review_title']}\n"
        f"Rating: {review['review_stars']}\n"
        f"Date: {review['review_date']}\n"
        f"Polarity: {review['textblob_polarity']:.2f}, "
        f"Subjectivity: {review['textblob_subjectivity']:.2f}\n"
        f"Review: {review['review_text']}\n"
        "---------------------------------------------\n"
    )
    text_area.insert(tk.INSERT, display_text)

def start_scraping_thread() -> None:
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
app.title("Amazon Review Analyzer")  

# Create and pack a label widget into the window, prompting for the Amazon product ID
label = tk.Label(app, text="Enter Amazon Product ID:")
label.pack()  

# Create and pack an entry widget for user input (to enter the product ID)
entry = tk.Entry(app)
entry.pack()  

# Create a button that, when clicked, will start the scraping process
scrape_button = tk.Button(app, text="Scrape Reviews", command=start_scraping_thread)
scrape_button.pack()

# Create and pack entry widgets for filter criteria
# Create and pack entry widgets for minimum and maximum subjectivity
min_subjectivity_label = tk.Label(app, text="Min Subjectivity (0 to 1):")
min_subjectivity_label.pack()
min_subjectivity_entry = tk.Entry(app)
min_subjectivity_entry.pack()

max_subjectivity_label = tk.Label(app, text="Max Subjectivity (0 to 1):")
max_subjectivity_label.pack()
max_subjectivity_entry = tk.Entry(app)
max_subjectivity_entry.pack()

# Create and pack entry widgets for minimum and maximum polarity
min_polarity_label = tk.Label(app, text="Min Polarity (-1 to 1):")
min_polarity_label.pack()
min_polarity_entry = tk.Entry(app)
min_polarity_entry.pack()

max_polarity_label = tk.Label(app, text="Max Polarity (-1 to 1):")
max_polarity_label.pack()
max_polarity_entry = tk.Entry(app)
max_polarity_entry.pack()

# Create a button to apply filters
filter_button = tk.Button(app, text="Apply Filters", command=apply_filters)
filter_button.pack()

# Create a scrolled text area where the scraped review data will be displayed
text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=40)
text_area.pack()

# Start the application's main event loop, ready for user interaction
app.mainloop()