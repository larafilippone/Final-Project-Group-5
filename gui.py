from scraping import scrape_amazon_reviews
import tkinter as tk
from tkinter import scrolledtext
import threading
import tkinter.font as tkFont
import os
import pandas as pd


# Initialize all_results as an empty list.
all_results = []

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_from_csv(filename):
    return pd.read_csv(filename)

def check_and_load_or_scrape(product_id):
    """
    Checks if data for the given product ID is already saved, loads it if so,
    otherwise scrapes new data from Amazon.

    Arguments:
    product_id (str): Amazon product ID.

    Returns:
    list: a list of dictionaries, each containing data about a review.
    """
    filename = f"{product_id}_reviews.csv"
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            return df.to_dict(orient='records'), True  # Convert DataFrame to list of dictionaries
        except Exception as e:
            print(f"Error loading data: {e}")
            return [], False
    else:
        urls = [f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}" for page in range(1, 11)]
        scraped_data = scrape_amazon_reviews(urls)
        save_to_csv(scraped_data, filename)  # Save the scraped data
        return scraped_data, False

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
        scrape_button.config(state=tk.NORMAL)
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    # Check if data is already saved and load it, otherwise scrape new data
    all_results, data_loaded = check_and_load_or_scrape(product_id)
    if not data_loaded:
        save_to_csv(all_results, f"{product_id}_reviews.csv")

    # Display the reviews
    for review in all_results[:10]:
        display_review(review)

    # Re-enable the scrape button
    scrape_button.config(state=tk.NORMAL)

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
                   rating, date, polarity, subjectivity, and review text.

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

# Frame for the subjectivity filters
subjectivity_frame = tk.Frame(app)
min_subjectivity_label = tk.Label(subjectivity_frame, text="Min Subjectivity (0 to 1):")
min_subjectivity_label.pack(side=tk.LEFT)
min_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
min_subjectivity_entry.pack(side=tk.LEFT)

max_subjectivity_label = tk.Label(subjectivity_frame, text="Max Subjectivity (0 to 1):")
max_subjectivity_label.pack(side=tk.LEFT)
max_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
max_subjectivity_entry.pack(side=tk.LEFT)
subjectivity_frame.pack(pady=(5, 5))  # Add some vertical padding

# Define a smaller font for explanations
explanation_font = tkFont.Font(size=9)

# Subjectivity explanation 
subjectivity_explanation_text = (
    "The subjectivity score measures how subjective or opinionated\n"
    "the review is, and ranges from 0 (completely objective) to 1\n"
    "(completely subjective)."
)
subjectivity_explanation = tk.Label(app, text=subjectivity_explanation_text, font=explanation_font)
subjectivity_explanation.pack()

# Frame for the polarity filters
polarity_frame = tk.Frame(app)
min_polarity_label = tk.Label(polarity_frame, text="Min Polarity (-1 to 1):")
min_polarity_label.pack(side=tk.LEFT)
min_polarity_entry = tk.Entry(polarity_frame, width=5)
min_polarity_entry.pack(side=tk.LEFT)

max_polarity_label = tk.Label(polarity_frame, text="Max Polarity (-1 to 1):")
max_polarity_label.pack(side=tk.LEFT)
max_polarity_entry = tk.Entry(polarity_frame, width=5)
max_polarity_entry.pack(side=tk.LEFT)
polarity_frame.pack(pady=(5, 5))  # Add some vertical padding

# Polarity explanation
polarity_explanation_text = (
    "The polarity score measures how negative or positive the sentiment\n"
    "of the review is, and ranges from -1 (extremely negative) to 1\n"
    "(extremely positive)."
)
polarity_explanation = tk.Label(app, text=polarity_explanation_text, font=explanation_font)
polarity_explanation.pack()

# Create a button to apply filters
filter_button = tk.Button(app, text="Apply Filters", command=apply_filters)
filter_button.pack()

# Create a scrolled text area where the scraped review data will be displayed
text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=40)
text_area.pack()

# Start the application's main event loop, ready for user interaction
app.mainloop()