from scraping import scrape_amazon_reviews
from product_search import get_amazon_product_data
from chatgpt import ask_chatgpt
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import tkinter.font as tkFont
import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List, Dict, Tuple, Any, Optional
from product_description import scrape_amazon_product_description

# Global variables initialization
all_results: List[Dict] = []
product_df = pd.DataFrame()
product_id: Optional[str] = None

# Dictionary mapping search_param options to corresponding categories on the Amazon website 
search_params = {
    " ": "All",
    "arts-crafts-intl-ship": "Arts & Crafts",
    "automotive-intl-ship": "Automotive",
    "baby-products-intl-ship": "Baby",
    "beauty-intl-ship": "Beauty & Personal Care",
    "stripbooks-intl-ship": "Books",
    "fashion-boys-intl-ship": "Boys' Fashion",
    "computers-intl-ship": "Computers",
    "deals-intl-ship": "Deals",
    "digital-music": "Digital Music",
    "electronics-intl-ship": "Electronics",
    "fashion-girls-intl-ship": "Girls' Fashion",
    "hpc-intl-ship": "Health & Household",
    "kitchen-intl-ship": "Home & Kitchen",
    "industrial-intl-ship": "Industrial & Scientific",
    "digital-text": "Kindle Store",
    "luggage-intl-ship": "Luggage",
    "fashion-mens-intl-ship": "Men's Fashion",
    "movies-tv-intl-ship": "Movies & TV",
    "music-intl-ship": "Movies, CDs & Vinyl",
    "pets-intl-ship": "Pet Supplies",
    "instant-video": "Prime Video",
    "software-intl-ship": "Software",
    "sporting-intl-ship": "Sports & Outdoors",
    "tools-intl-ship": "Tools & Home Improvement",
    "toys-and-games-intl-ship": "Toys & Games",
    "videogames-intl-ship": "Video Games",
    "fashion-womens-intl-ship": "Women's Fashion"
}

# Create a function to check if the given product ID is valid
def is_valid_asin(asin: str) -> bool:
    """
    Validates if the given string is a valid ASIN.

    Arguments:
    asin (str): string to be validated as ASIN.

    Returns:
    bool: true if the string is a valid ASIN, False otherwise.
    """
    return len(asin) == 10 and asin.isalnum()

# Create a function to save scraped data to CSV file
def save_to_csv(data: List[Dict], filename: str) -> None:
    """
    Saves the scraped review data to a CSV file.

    This function takes the scraped data, which is a list of dictionaries where each dictionary represents a review,
    and converts it into a pandas DataFrame. It then saves this DataFrame to a CSV file with the specified filename.
    The index of the DataFrame is not included in the CSV file. After saving, a confirmation message is printed.

    Arguments:
    data (list of dict): the scraped review data, where each review is represented as a dictionary.
    filename (str): the name of the file to which the data will be saved. The file will be saved in the current
                    working directory unless a different path is specified in the filename.

    Returns:
    None: this function does not return any value but saves data to a CSV file and prints a confirmation message.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Create a function to load data from CSV file into a pandas DataFrame
def load_from_csv(filename: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.

    This function reads a CSV file specified by the filename and loads its contents into a pandas DataFrame. 
    It assumes that the CSV file is properly formatted and that the first row contains the header names for the columns. 
    The function is primarily used to load scraped review data that has been previously saved to a CSV file.

    Arguments:
    filename (str): the name of the CSV file to be loaded. The file should be in the current working directory 
                    or include the full path.

    Returns:
    pd.DataFrame: a pandas DataFrame containing the data loaded from the CSV file.
    """
    return pd.read_csv(filename)

# Create a function to either load data from CSV file or scrape new data
def check_and_load_or_scrape(product_id: str) -> Tuple[List[Dict], bool]:
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

# Create a function to run the scraping process
def run_scraping() -> None:
    """
    Retrieves and displays Amazon product reviews based on the entered product ID. 
    The display includes the review's title, rating, date, product specifics, 
    sentiment analysis scores (polarity and subjectivity), and the review text itself.

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

    if not product_id or not is_valid_asin(product_id):
        text_area.insert(tk.INSERT, "Please enter a valid product ID.\n")
        scrape_button.config(state=tk.NORMAL)
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    # Check if data is already saved and load it, otherwise scrape new data
    all_results, data_loaded = check_and_load_or_scrape(product_id)
    if not data_loaded:
        save_to_csv(all_results, f"{product_id}_reviews.csv")

    # Check if there are any reviews
    if not all_results:  # all_results is empty
        text_area.insert(tk.INSERT, "This product has no reviews.\n")
    else:
        # Display the reviews
        for review in all_results[:10]:
            display_review(review)
        # Display the results from Chat GPT

        display_chatgpt(all_results)

    # Re-enable the scrape button
    scrape_button.config(state=tk.NORMAL)

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

    text_area.delete('1.0', tk.END)  # Clear the existing text

    filtered_reviews = [review for review in all_results
                        if min_subjectivity <= review['textblob_subjectivity'] <= max_subjectivity
                        and min_polarity <= review['textblob_polarity'] <= max_polarity]

    if not filtered_reviews:  # Check if the filtered list is empty
        text_area.insert(tk.INSERT, "No reviews matching the filtering criteria.\n")
    else:
        for review in filtered_reviews[:10]:  # Display up to 10 of the filtered reviews
            display_review(review)

# Create a function to display a single review in the GUI
def display_review(review: Dict[str, Any]) -> None:
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

def display_chatgpt(all_results):
    """
    Generates the summary and improvements and displays it 
    """

    # Loop through the list of dictionaries to generate a string for use of chatgpt 
    reviews_string = ""
    for review in all_results:
        reviews_string += (
            f"Title: {review['review_title']}\n"
            f"Date: {review['review_date']}\n"
            f"Review: {review['review_text']}\n"
    )

    # Generate and display summary 
    request_summary = f"Summarize the negative and positive sentiment of the reviews attached. Limit to 6 bullet points.  {reviews_string}. "

    # limited lenght of input for Chat GPT API allowed - limit the lenght of the string to 4000 tokens
    request_summary = request_summary[:4000]
    review_summary_text.insert(tk.INSERT, f"Generating summary of the reviews...")
    response_chatgpt = ask_chatgpt(request_summary)
    review_summary_text.delete("1.0", tk.END)  # Delete all existing content
    review_summary_text.insert(tk.INSERT, response_chatgpt)

    # Generate and display product improvement suggestions 
    request_summary = f"Please generate product improvement suggestions based on the negative points raised in the following reviews. Only display precise suggestions, no additional text. Limit to 4 suggestions. {reviews_string}. "

    # limited lenght of input for Chat GPT API allowed - limit the lenght of the string to 4000 tokens
    request_summary = request_summary[:4000]
    product_improvement_text.insert(tk.INSERT, f"Generating product improvement suggestions...")
    response_chatgpt = ask_chatgpt(request_summary)
    product_improvement_text.delete("1.0", tk.END)  # Delete all existing content
    product_improvement_text.insert(tk.INSERT, response_chatgpt)


# Create a function to display a wordcloud in the GUI
def display_wordcloud() -> None:
    """
    Generates and displays a word cloud from the scraped reviews, excluding common stopwords.

    Arguments:
    None: this function uses global variable all_results.

    Returns:
    None: this function updates the GUI with the word cloud image.
    """
    # NLTK Stop words
    stop_words = set(stopwords.words('english'))

    # Combine all review texts into a single string
    text = " ".join(review['review_text'] for review in all_results)

    # Tokenize the text and remove stopwords
    words = word_tokenize(text)
    filtered_text = " ".join(word for word in words if word.lower() not in stop_words and word.isalpha())

    # Generate the word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color='white').generate(filtered_text)

    # Convert to an image and display in Tkinter
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Create a function to start a new thread and run the scraping process
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

def on_select(event: tk.Event) -> None:

    """
    On selection of a row of the treeview widget 

    Arguments:
    - event (Tkinter Event): The event object triggered by the Treeview selection.

    Returns:
    - None: Prints the selected URL and assigns it to the global variable 'selection_url'.
    """
    global product_id

    selected_item = products_tree.selection()[0]
    selected_index = products_tree.index(selected_item)
    product_id = product_df.loc[selected_index, 'ASIN']
    product_url = product_df.loc[selected_index, 'Product URL']

    product_text_scrape = scrape_amazon_product_description(product_url)

    product_text.delete(1.0, tk.END)
    if product_text:
        product_text.insert(tk.END, product_text_scrape)

    else:
        product_text.insert(tk.END, "This product has no description.")
    
    # Enable the scrape button when a product is selected
    scrape_button.config(state=tk.NORMAL)

    print(f"Selected ASIN: {product_id}")

# Create function to update the Treeview widget
def update_treeview(keyword: str, search_param: str, num_pages: int) -> None:
    """
    Updates a Tkinter Treeview widget with Amazon product data obtained from the search 

    Arguments:
    - keyword (str): the search keyword inserted by the user 
    - search_param (str): the search parameter (e.g., 'Books', 'Electronics') which is equivalent to the Amazon homepage  
    - num_pages (int): the number of pages to scrape (default is 1 to not pulling to many requests and get blocked) 

    Returns:
    - None: creates treeview table and saves results in the csv file "amazon_product_data.csv"
    """
    global product_df

    # Create an empty DataFrame to store the product data 
    product_df = pd.DataFrame(columns=["Number", "Product Name", "Product URL", "ASIN"])

    # Update DataFrame
    product_data = get_amazon_product_data(keyword, search_param, num_pages)
    product_df = pd.concat([product_df, pd.DataFrame(product_data)], ignore_index=True)

    # Clear previous results in Treeview
    for row in products_tree.get_children():
        products_tree.delete(row)

    if not product_df.empty:
        # Insert data into Treeview
        for i, row in product_df.iterrows():
            products_tree.insert("", "end", values=(i + 1, row["Product Name"], row["Product URL"], row["ASIN"]))

        # Save DataFrame to CSV
        product_df.to_csv('amazon_product_data.csv', index=False)



# Initialize the main application window using Tkinter
app = tk.Tk()
app.title("Amazon Review Analyzer")  
app.geometry("3024x1964")

# Create frames for the left and right sides
left_frame = tk.Frame(app, borderwidth=2, relief="groove")
right_frame = tk.Frame(app, borderwidth=2, relief="groove")

left_frame.grid(row=0, column=0, sticky="nswe")
right_frame.grid(row=0, column=1, sticky="nswe")

# Configure the grid
app.grid_columnconfigure(0, weight=1, uniform="group1")
app.grid_columnconfigure(1, weight=1, uniform="group1")
app.grid_rowconfigure(0, weight=1)

# Populate the left frame
tk.Label(left_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
keyword_entry = tk.Entry(left_frame)
keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Create widgets for search parameter and number of pages
tk.Label(app, text="Search Parameter:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Label(app, text="Number of Pages:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Create dropdown menu for search_param
search_param_var = tk.StringVar()
search_param_dropdown = ttk.Combobox(left_frame, textvariable=search_param_var, values=list(search_params.values()))
search_param_dropdown.set(list(search_params.values())[0])  # Set default value
search_param_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Create entry to set the number of pages
num_pages_entry = tk.Entry(left_frame)
num_pages_entry.grid(row=2, column=1, padx=5, pady=5)

# Create button to start the search
search_button = tk.Button(left_frame, text="Search Amazon", command=lambda: update_treeview(keyword_entry.get(), value_to_key(search_param_var.get()), int(num_pages_entry.get())))
search_button.grid(row=3, column=0, columnspan=2, pady=10)

#Returns the key for the value of the search_params dictionary - to sort out the problem that the value should be display in the dropdown but the key used for the search
def value_to_key(search_value):

    for key, value in search_params.items():
        if value == search_value:
            print(key)
            return key

# Treeview for displaying product list
products_tree = ttk.Treeview(left_frame, columns=("Number", "Product Name", "Product URL", "ASIN"), show="headings")
products_tree.heading("Number", text="Number")
products_tree.heading("Product Name", text="Product Name")
products_tree.heading("Product URL", text="Product URL")
products_tree.heading("ASIN", text="ASIN")
products_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Bind the on_select function to the Treeview's selection event
products_tree.bind("<<TreeviewSelect>>", on_select)

# Create a button that, when clicked, will start the scraping process
scrape_button = tk.Button(left_frame, text="Scrape Reviews", command=start_scraping_thread, state=tk.DISABLED)
scrape_button.grid(row=6, column=0, columnspan=2, pady=5)

# Frame for the subjectivity filters
subjectivity_frame = tk.Frame(left_frame)
min_subjectivity_label = tk.Label(subjectivity_frame, text="Min Subjectivity (0 to 1):")
min_subjectivity_label.pack(side=tk.LEFT)
min_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
min_subjectivity_entry.pack(side=tk.LEFT)

max_subjectivity_label = tk.Label(subjectivity_frame, text="Max Subjectivity (0 to 1):")
max_subjectivity_label.pack(side=tk.LEFT)
max_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
max_subjectivity_entry.pack(side=tk.LEFT)
subjectivity_frame.grid(row=7, column=0, columnspan=2, pady=(5, 5))

# Define a smaller font for explanations
explanation_font = tkFont.Font(size=9)

# Subjectivity explanation 
subjectivity_explanation_text = (
    "Subjectivity score measures how subjective or opinionated the review is,\n"
    "and ranges from 0 (completely objective) to 1 (completely subjective)."
)
subjectivity_explanation = tk.Label(left_frame, text=subjectivity_explanation_text, font=explanation_font, width = 100)
subjectivity_explanation.grid(row=8, column=0, columnspan=2, pady=(5, 5))

# Frame for the polarity filters
polarity_frame = tk.Frame(left_frame)
min_polarity_label = tk.Label(polarity_frame, text="Min Polarity (-1 to 1):")
min_polarity_label.pack(side=tk.LEFT)
min_polarity_entry = tk.Entry(polarity_frame, width=5)
min_polarity_entry.pack(side=tk.LEFT)

max_polarity_label = tk.Label(polarity_frame, text="Max Polarity (-1 to 1):")
max_polarity_label.pack(side=tk.LEFT)
max_polarity_entry = tk.Entry(polarity_frame, width=5)
max_polarity_entry.pack(side=tk.LEFT)
polarity_frame.grid(row=9, column=0, columnspan=2, pady=(5, 5))

# Polarity explanation
polarity_explanation_text = (
    "Polarity score measures how negative or positive the sentiment of the review is,\n"
    "and ranges from -1 (extremely negative) to 1 (extremely positive)."
)
polarity_explanation = tk.Label(left_frame, text=polarity_explanation_text, font=explanation_font)
polarity_explanation.grid(row=10, column=0, columnspan=2, pady=(5, 10))

# Create a button to apply filters
filter_button = tk.Button(left_frame, text="Apply Filters", command=apply_filters)
filter_button.grid(row=11, column=0, columnspan=2, pady=5)

# Create a button to display the word cloud
wordcloud_button = tk.Button(left_frame, text="Show Word Cloud", command=display_wordcloud)
wordcloud_button.grid(row=12, column=0, columnspan=2, pady=5)

# Create a scrolled text area where the scraped review data will be displayed
text_area = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=100, height=40)
text_area.grid(row=13, column=0, columnspan=2, pady=10)

# Create a label for the Product Description
product_text_label = tk.Label(right_frame, text="Product Description:")
product_text_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")

# Create a text field for displaying the Product Description
product_text = tk.Text(right_frame, wrap=tk.WORD, width=90, height=10)  
product_text.grid(row=4, column=2, padx=5, pady=5)

# Create a label for the Review Summary
review_summary_label = tk.Label(right_frame, text="Review Summary:")
review_summary_label.grid(row=5, column=2, padx=5, pady=5, sticky="e")

# Create a text field for displaying the Review Summary
review_summary_text = tk.Text(right_frame, wrap=tk.WORD, width=90, height=10) 
review_summary_text.grid(row=6, column=2, padx=5, pady=5)

# Create a label for Product Improvement Suggestions
product_improvement_label = tk.Label(right_frame, text="Product Improvement Suggestions:")
product_improvement_label.grid(row=7, column=2, padx=5, pady=5, sticky="e")

# Create a text field for displaying Product Improvement Suggestions
product_improvement_text = tk.Text(right_frame, wrap=tk.WORD, width=90, height=10)  
product_improvement_text.grid(row=8, column=2, padx=5, pady=5)

# Start the application's main event loop, ready for user interaction
app.mainloop()