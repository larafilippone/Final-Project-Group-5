"""
main.py: This script serves as the entry point of the Amazon Review Analyzer application. 
It contains the main GUI setup using Tkinter, event handling, and orchestration of various components.
"""

import threading
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from typing import Dict, List, Any
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import pandas as pd

from chatgpt_integration import ask_chatgpt
from config import SEARCH_PARAMS
from data_analysis import get_polarity_color, generate_filtered_text
from scraping_utils import get_amazon_product_data, scrape_amazon_product_description, scrape_data
from utils import is_valid_asin, open_amazon, value_to_key

# Initialize global variables
all_results: List[Dict[str, Any]] = []
product_df = pd.DataFrame()
product_id: str = ""
product_url = ""


# Function definitions
def display_review(review: dict) -> None:
    """
    Displays a single review in the text area of the GUI.

    This function formats the details of a review and appends it to the text area widget
    for display. It includes the title, rating, date, polarity, subjectivity, and the review
    text itself. Each review is separated by a line of dashes for clarity.

    Arguments:
    review (dict): a dictionary containing the details of a review. Expected keys are
                   'review_title', 'review_stars', 'review_date', 'textblob_polarity',
                   'textblob_subjectivity', and 'review_text'.

    Returns:
    None: this function does not return a value but updates the GUI directly.
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


# Create a function to add filtering functionalities in the GUI
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

    text_area.delete("1.0", tk.END)  # Clear the existing text

    filtered_reviews = [
        review
        for review in all_results
        if min_subjectivity <= review["textblob_subjectivity"] <= max_subjectivity
        and min_polarity <= review["textblob_polarity"] <= max_polarity
    ]

    if not filtered_reviews:  # Check if the filtered list is empty
        text_area.insert(tk.INSERT, "No reviews matching the filtering criteria.\n")
    else:
        for review in filtered_reviews[:10]:  # Display up to 10 of the filtered reviews
            display_review(review)


# Create function to display average polarity and corresponding color
def display_average_polarity_and_color() -> None:
    """
    This function computes the average polarity of all reviews and displays it on the GUI. It also
    shows a colored circle: red for negative sentiment, green for positive, and orange for neutral.
    If there are no reviews to analyze, it updates the GUI to indicate that no average can be calculated.

    Arguments:
    None: this function uses the global variable 'all_results' to access the review data.

    Returns:
    None: this function does not return any value but updates the GUI directly.
    """
    if all_results:
        average_polarity, color = get_polarity_color(all_results)
        polarity_text = f"Average Polarity Score: {average_polarity:.2f}"
        polarity_label.config(text=polarity_text)
        polarity_canvas.delete("all")
        polarity_canvas.create_oval(5, 5, 40, 40, fill=color, outline=color)
    else:
        polarity_label.config(text="No reviews available to calculate average polarity.")
        polarity_canvas.delete("all")


# Create a function to display the text generated by ChatGPT
def display_chatgpt(all_results: List[Dict[str, str]]) -> None:
    """
    Generates a summary of reviews and product improvement suggestions using the ChatGPT API
    and displays them in the respective text areas of the application.

    Arguments:
    all_results (List[Dict[str, str]]): a list of dictionaries, where each dictionary contains data
    about a review, such as the title, date, and text.

    Returns:
    None: this function does not return any value. It updates the text areas in the GUI directly
    with the content generated by the ChatGPT API.
    """

    # Loop through the list of dictionaries to generate a string for use of chatgpt
    reviews_string = ""
    for review in all_results:
        reviews_string += (
            f"Title: {review['review_title']}\n" f"Date: {review['review_date']}\n" f"Review: {review['review_text']}\n"
        )

    # Generate and display summary
    request_summary = (
        "Summarize the negative and positive sentiment of the reviews attached. "
        "Limit to 6 bullet points. "
        f"{reviews_string}."
    )
    # limited length of input for Chat GPT API allowed - limit the length of the string to 4000 tokens
    request_summary = request_summary[:4000]
    review_summary_text.delete("1.0", tk.END)  # Delete all existing content
    review_summary_text.insert(tk.INSERT, "Generating summary of the reviews...")
    product_improvement_text.delete("1.0", tk.END)  # Delete all existing content
    product_improvement_text.insert(tk.INSERT, "Generating product improvement suggestions...")
    response_chatgpt = ask_chatgpt(request_summary)
    review_summary_text.delete("1.0", tk.END)  # Delete all existing content
    review_summary_text.insert(tk.INSERT, response_chatgpt)

    # Generate and display product improvement suggestions
    request_summary = (
        "Please generate product improvement suggestions based on the negative points "
        "raised in the following reviews. Only display precise suggestions, no additional "
        "text. Limit to 4 suggestions. "
        f"{reviews_string}."
    )

    # limited lenght of input for Chat GPT API allowed - limit the lenght of the string to 4000 tokens
    request_summary = request_summary[:4000]
    response_chatgpt = ask_chatgpt(request_summary)
    product_improvement_text.delete("1.0", tk.END)  # Delete all existing content
    product_improvement_text.insert(tk.INSERT, response_chatgpt)


# Create a function to display the word cloud
def display_wordcloud(all_results: List[Dict[str, Any]]) -> None:
    """
    Generates and displays a word cloud from the scraped reviews, visualizing the frequency of words used in the reviews.

    Arguments:
    all_results (List[Dict[str, Any]]): a list of dictionaries where each dictionary contains the data of a review.
                                        Each dictionary should have a key 'review_text' containing the text of the review.

    Returns:
    None: this function does not return any value. It directly displays the word cloud image or 
            prints a message if there are no words to display.
    """
    filtered_text = generate_filtered_text(all_results)

    if not filtered_text:
        print("No words left after filtering for the word cloud.")
        return

    # Generate the word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate(filtered_text)

    # Convert to an image and display in Tkinter
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# Create function to select a single product from the treeview widget
def on_select(event: tk.Event) -> None:
    """
    Handles the selection of a product from the products_tree Treeview widget. When a product is selected,
    this function retrieves the selected product's ASIN and URL, and then attempts to scrape the product's
    description from Amazon. The scraped description (or a message indicating the absence of a description)
    is then displayed in the product_text Text widget. It also enables the scrape button.

    Arguments:
    event: the event that triggered this function, passed automatically by the Tkinter event handler.

    Returns:
    None: this function does not return any value but updates the GUI elements and global variables.
    """

    global product_id, product_url

    selected_items = products_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        selected_index = products_tree.index(selected_item)
        product_id = product_df.loc[selected_index, "ASIN"]
        product_url = product_df.loc[selected_index, "Product URL"]

        product_text_scrape = scrape_amazon_product_description(product_url)

        product_text.delete(1.0, tk.END)
        if product_text_scrape:
            product_text.insert(tk.END, product_text_scrape)
        else:
            product_text.insert(tk.END, "This product has no description.")

        scrape_button.config(state=tk.NORMAL)


# Create function to update the treeview widget
def update_treeview(keyword: str, search_param: str, num_pages: int) -> None:
    """
    Updates the Treeview widget (products_tree) with product data based on the specified search parameters.
    It creates a DataFrame to hold the product data, fetches data from Amazon using the
    get_amazon_product_data function, and then populates the Treeview with this data. Each row in the
    Treeview represents a product, showing its number, name, and ASIN.

    Arguments:
    keyword (str): the search keyword entered by the user.
    search_param (str): the search parameter/category selected by the user.
    num_pages (int): the number of pages to scrape for product data.

    Returns:
    None: this function does not return any value but updates the products_tree Treeview and the global variable.
    """

    global product_df
    
    product_df = pd.DataFrame(columns=["Number", "Product Name", "Product URL", "ASIN"])
    product_data = get_amazon_product_data(keyword, search_param, num_pages)
    product_df = pd.concat([product_df, pd.DataFrame(product_data)], ignore_index=True)

    for row in products_tree.get_children():
        products_tree.delete(row)

    if not product_df.empty:
        for i, row in product_df.iterrows():
            products_tree.insert("", "end", values=(i + 1, row["Product Name"], row["ASIN"]))


# Create a function to run the scraping process
def run_scraping() -> None:
    """
    Manages the process of scraping reviews for a specified product ID. It validates the product ID,
    retrieves the number of review pages to scrape, calls the scrape_data function to scrape reviews,
    and updates the GUI with the scraped reviews.

    The function disables the scrape button during the scraping process to prevent concurrent scraping,
    and re-enables it upon completion. It also updates the global variable 'all_results' with the
    scraped reviews.

    If no valid product ID is provided, or there are no reviews for the product, or an error occurs during scraping,
    the function updates the text area in the GUI with an appropriate message.

    Arguments:
    None: this function relies on global variables and GUI components (like product_id and review_pages_entry).

    Returns:
    None: this function does not return any value but updates the GUI and global variables.
    """
    global all_results, product_id

    # Disable the scrape button to prevent concurrent scraping
    scrape_button.config(state=tk.DISABLED)
    text_area.delete("1.0", tk.END)

    if not product_id or not is_valid_asin(product_id):
        text_area.insert(tk.INSERT, "Please enter a valid product ID.\n")
        scrape_button.config(state=tk.NORMAL)
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    try:
        num_review_pages = int(review_pages_entry.get())
    except ValueError:
        text_area.insert(tk.INSERT, "Please enter a valid number of review pages.\n")
        scrape_button.config(state=tk.NORMAL)
        return

    all_results = scrape_data(product_id, num_review_pages)

    if not all_results:
        text_area.insert(tk.INSERT, "This product has no reviews or there was an error in scraping.\n")
    else:
        for review in all_results[:10]:
            display_review(review)
        display_average_polarity_and_color()
        display_chatgpt(all_results)

    scrape_button.config(state=tk.NORMAL)


# Create function to start a separate thread
def start_scraping_thread() -> None:
    """
    Initiates the review scraping process in a separate thread. This function creates a new thread
    targeting the 'run_scraping' function, which handles the scraping of Amazon product reviews.

    The use of threading prevents the GUI from becoming unresponsive during the scraping process,
    allowing the main application thread to continue running and managing user interactions.

    Arguments:
    None: this function does not take any arguments.

    Returns:
    None: this function does not return any value. It starts a new thread for the scraping process.
    """
    scraping_thread = threading.Thread(target=run_scraping)
    scraping_thread.start()


# Initialize the main application window using Tkinter
app = tk.Tk()
app.title("Amazon Review Analyzer")

# Get the laptop screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate the application window size
app_width = int(screen_width)
app_height = int(screen_height)

# Center the application window on the screen
x_position = int((screen_width - app_width) / 2)
y_position = int((screen_height - app_height) / 2)

# Set the geometry of the application window
app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")

sf_pro_font = tkFont.Font(family="SF Pro", size=12, weight=tkFont.NORMAL)

# Create frames for the left and right sides
left_frame = tk.Frame(app, borderwidth=0, relief="flat")
right_frame = tk.Frame(app, borderwidth=0, relief="flat")

left_frame.grid(row=0, column=0, sticky="nswe")
right_frame.grid(row=0, column=1, sticky="nswe")

# Configure the grid to have equal column widths
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_columnconfigure(1, weight=1)

# Configure the grid to have equal column widths
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

# Configure the grid
app.grid_columnconfigure(0, weight=1, uniform="group1")
app.grid_columnconfigure(1, weight=1, uniform="group1")
app.grid_rowconfigure(0, weight=1)

# Populate the left frame
tk.Label(left_frame, text="Keyword / ASIN:").grid(row=0, column=0, padx=110, pady=20, sticky="w")
keyword_entry = tk.Entry(left_frame)
keyword_entry.grid(row=0, column=1, pady=20, sticky="w")

# Create widgets for search parameter and number of pages
tk.Label(left_frame, text="Search Parameter:").grid(row=1, column=0, padx=110, pady=5, sticky="w")
tk.Label(left_frame, text="Number of Pages:").grid(row=2, column=0, padx=110, pady=5, sticky="w")

# Create dropdown menu for search_param
search_param_var = tk.StringVar()
search_param_dropdown = ttk.Combobox(
    left_frame,
    textvariable=search_param_var,
    values=list(SEARCH_PARAMS.values()),
    state="readonly",  # Set the Combobox state to readonly
)
search_param_dropdown.set(list(SEARCH_PARAMS.values())[0])
search_param_dropdown.grid(row=1, column=1, pady=5, sticky="w")

# Create entry to set the number of pages
num_pages_entry = tk.Entry(left_frame, width=5)
num_pages_entry.grid(row=2, column=1, pady=5, sticky="w")

# Set default value to 1
num_pages_entry.insert(0, "1")

# Create button to start the search
search_button = tk.Button(
    left_frame,
    text="Search Amazon",
    command=lambda: update_treeview(
        keyword_entry.get(), value_to_key(search_param_var.get()), int(num_pages_entry.get())
    ),
)
search_button.grid(row=3, column=0, columnspan=2, padx=300, pady=20, sticky="w")

# Treeview to display the product list - the search result
products_tree = ttk.Treeview(left_frame, columns=("Number", "Product Name", "ASIN"), show="headings")
products_tree.heading("Number", text="Number")
products_tree.heading("Product Name", text="Product Name")
products_tree.heading("ASIN", text="ASIN")
products_tree.grid(row=4, column=0, columnspan=2, padx=15, pady=15, sticky="w")

# Configure the column widths
products_tree.column("Number", width=100, anchor="center")
products_tree.column("Product Name", width=445, anchor="w")
products_tree.column("ASIN", width=140, anchor="w")

# Bind the on_select function to the Treeview's selection event - when a product is actually selected
products_tree.bind("<<TreeviewSelect>>", on_select)

# Create a label for the Product Description field
product_text_label = tk.Label(left_frame, text="Product Description:")
product_text_label.grid(row=5, column=0, padx=15, pady=5, sticky="w")

# Create a text field for displaying the Product Description
product_text = tk.Text(left_frame, wrap=tk.WORD, height=8, width=85, font=sf_pro_font)
product_text.grid(row=6, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Create a button to go to the selected Amazon product homepage
go_to_amazon_button = tk.Button(left_frame, text="Go to Amazon", command=lambda: open_amazon(product_url))
go_to_amazon_button.grid(row=7, column=0, columnspan=2, padx=320, pady=5, sticky="w")

# Label and entry for number of review pages
tk.Label(right_frame, text="Number of Review Pages:").grid(row=1, column=0, pady=20, sticky="e")
review_pages_entry = tk.Entry(right_frame, width=5)
review_pages_entry.grid(row=1, column=1, padx=1, pady=20, sticky="w")

# Set default value to 1
review_pages_entry.insert(0, "1")

# Create a button that, when clicked, will start the scraping process
scrape_button = tk.Button(
    right_frame, text="Scrape Reviews and Analyze", command=start_scraping_thread, state=tk.DISABLED
)
scrape_button.grid(row=1, column=1, padx=106, pady=20, sticky="w")

# Create a text area where the scraped review data will be displayed
text_area = tk.Text(right_frame, wrap=tk.WORD, width=85, height=10, font=sf_pro_font)
text_area.grid(row=2, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Frame for the subjectivity filters
subjectivity_frame = tk.Frame(right_frame)
subjectivity_frame.grid(row=3, column=0, columnspan=1, pady=(5, 5), sticky="ew")
min_subjectivity_label = tk.Label(subjectivity_frame, text="Min Subjectivity (0 to 1):", font=tkFont.Font(size=9))
min_subjectivity_label.grid(row=0, column=0, padx=20, pady=2, sticky="w")
min_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
min_subjectivity_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

max_subjectivity_label = tk.Label(subjectivity_frame, text="Max Subjectivity (0 to 1):", font=tkFont.Font(size=9))
max_subjectivity_label.grid(row=1, column=0, padx=20, pady=2, sticky="w")
max_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
max_subjectivity_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

# Subjectivity explanation
SUBJECTIVITY_EXPLANATION_TEXT = (
    "Subjectivity score measures how subjective or opinionated the review is,\n"
    "and ranges from 0 (completely objective) to 1 (completely subjective)."
)
subjectivity_explanation = tk.Label(
    right_frame, text=SUBJECTIVITY_EXPLANATION_TEXT, font=tkFont.Font(size=9), justify="left"
)
subjectivity_explanation.grid(row=3, column=1, padx=1, pady=1, sticky="w")

# Frame for the polarity filters
polarity_frame = tk.Frame(right_frame)
polarity_frame.grid(row=4, column=0, columnspan=1, pady=(5, 5), sticky="ew")
min_polarity_label = tk.Label(polarity_frame, text="Min Polarity (-1 to 1):", font=tkFont.Font(size=9))
min_polarity_label.grid(row=0, column=0, padx=20, pady=2, sticky="w")
min_polarity_entry = tk.Entry(polarity_frame, width=5)
min_polarity_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

max_polarity_label = tk.Label(polarity_frame, text="Max Polarity (-1 to 1):", font=tkFont.Font(size=9))
max_polarity_label.grid(row=1, column=0, padx=20, pady=2, sticky="w")
max_polarity_entry = tk.Entry(polarity_frame, width=5)
max_polarity_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

# Polarity explanation
POLARITY_EXPLANATION_TEXT = (
    "Polarity score measures how negative or positive the sentiment of the review is,\n"
    "and ranges from -1 (extremely negative) to 1 (extremely positive)."
)
polarity_explanation = tk.Label(right_frame, text=POLARITY_EXPLANATION_TEXT, font=tkFont.Font(size=9), justify="left")
polarity_explanation.grid(row=4, column=1, padx=1, pady=1, sticky="w")

# Create a button to apply filters
filter_button = tk.Button(right_frame, text="Apply Filters", command=apply_filters)
filter_button.grid(row=5, column=0, columnspan=2, pady=1, padx=15, sticky="w")

# Canvas for displaying the polarity light
polarity_canvas = tk.Canvas(right_frame, width=40, height=40, bg="white")
polarity_canvas.grid(row=6, column=0, columnspan=2, padx=350, pady=10, sticky="w")

# Label for displaying average polarity
polarity_label = tk.Label(right_frame, text="Average Polarity Score: ", font=("Helvetica", 9))
polarity_label.grid(row=6, column=0, columnspan=2, padx=200, pady=10, sticky="w")

# Create a label for the Review Summary text field
review_summary_label = tk.Label(right_frame, text="Review Summary:")
review_summary_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")

# Create a text field for displaying the Review Summary
review_summary_text = tk.Text(right_frame, wrap=tk.WORD, width=85, height=8, font=sf_pro_font)
review_summary_text.grid(row=8, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Create a label for Product Improvement Suggestions text field
product_improvement_label = tk.Label(right_frame, text="Product Improvement Suggestions:")
product_improvement_label.grid(row=9, column=0, padx=20, pady=5, sticky="w")

# Create a text field for displaying Product Improvement Suggestions
product_improvement_text = tk.Text(right_frame, wrap=tk.WORD, width=85, height=8, font=sf_pro_font)
product_improvement_text.grid(row=10, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Create a button to display the word cloud
wordcloud_button = tk.Button(right_frame, text="Show Word Cloud", command=lambda: display_wordcloud(all_results))
wordcloud_button.grid(row=11, column=0, columnspan=2, padx=300, pady=5, sticky="w")

# Start the main event loop
app.mainloop()
