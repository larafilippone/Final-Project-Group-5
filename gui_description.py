# Import the packages
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
import webbrowser

# Initialize global variables 
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
    "electronics-intl-ship": "Electronics",
    "fashion-girls-intl-ship": "Girls' Fashion",
    "hpc-intl-ship": "Health & Household",
    "kitchen-intl-ship": "Home & Kitchen",
    "industrial-intl-ship": "Industrial & Scientific",
    "digital-text": "Kindle Store",
    "luggage-intl-ship": "Luggage",
    "fashion-mens-intl-ship": "Men's Fashion",
    "pets-intl-ship": "Pet Supplies",
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
def check_and_load_or_scrape(product_id: str, num_review_pages: int) -> Tuple[List[Dict], bool]:
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
        urls = [f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}" 
                for page in range(1, num_review_pages + 1)]
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
    global all_results, product_id

    # Disable the scrape button to prevent concurrent scraping
    scrape_button.config(state=tk.DISABLED)
    
    # Clear the previous results from the text area
    text_area.delete('1.0', tk.END)

    if not product_id or not is_valid_asin(product_id):
        text_area.insert(tk.INSERT, "Please enter a valid product ID.\n")
        scrape_button.config(state=tk.NORMAL)
        return

    text_area.insert(tk.INSERT, f"Scraping reviews for product ID: {product_id}...\n")

    # Retrieve the number of review pages from the entry, with a default value
    try:
        num_review_pages = int(review_pages_entry.get())
    except ValueError:
        text_area.insert(tk.INSERT, "Please enter a valid number of review pages.\n")
        scrape_button.config(state=tk.NORMAL)
        return

    # Use the num_review_pages in the check_and_load_or_scrape function
    all_results, data_loaded = check_and_load_or_scrape(product_id, num_review_pages)

    # Check if there are any reviews
    if not all_results:
        text_area.insert(tk.INSERT, "This product has no reviews or there was an error in scraping.\n")
    else:
        # Display the reviews
        for review in all_results[:10]:  # Display only the first 10 reviews for brevity
            display_review(review)

        # Display average polarity and emoji, if applicable
        display_average_polarity_and_color()

        # Display results from ChatGPT, if applicable
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
            f"Title: {review['review_title']}\n"
            f"Date: {review['review_date']}\n"
            f"Review: {review['review_text']}\n"
    )

    # Generate and display summary 
    request_summary = f"Summarize the negative and positive sentiment of the reviews attached. Limit to 6 bullet points.  {reviews_string}. "

    # limited length of input for Chat GPT API allowed - limit the length of the string to 4000 tokens
    request_summary = request_summary[:4000]
    review_summary_text.delete("1.0", tk.END)  # Delete all existing content
    review_summary_text.insert(tk.INSERT, f"Generating summary of the reviews...")
    product_improvement_text.delete("1.0", tk.END)  # Delete all existing content
    product_improvement_text.insert(tk.INSERT, f"Generating product improvement suggestions...")
    response_chatgpt = ask_chatgpt(request_summary)
    review_summary_text.delete("1.0", tk.END)  # Delete all existing content
    review_summary_text.insert(tk.INSERT, response_chatgpt)

    # Generate and display product improvement suggestions 
    request_summary = f"Please generate product improvement suggestions based on the negative points raised in the following reviews. Only display precise suggestions, no additional text. Limit to 4 suggestions. {reviews_string}. "

    # limited lenght of input for Chat GPT API allowed - limit the lenght of the string to 4000 tokens
    request_summary = request_summary[:4000]
    response_chatgpt = ask_chatgpt(request_summary)
    product_improvement_text.delete("1.0", tk.END)  # Delete all existing content
    product_improvement_text.insert(tk.INSERT, response_chatgpt)

# Create function to calculate average polarity score and output corresponding color
def get_polarity_color(reviews: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    This function iterates through the list of reviews, sums up their polarity scores, and calculates 
    the average polarity. Based on the average polarity, it assigns a color: red for negative sentiment 
    (average polarity less than -0.25), green for positive sentiment (average polarity greater than 0.25), 
    and orange for neutral sentiment (average polarity between -0.25 and 0.25).

    Arguments:
    reviews (List[Dict[str, Any]]): a list of dictionaries, where each dictionary represents a review 
                                    and contains at least a 'textblob_polarity' key with a numeric polarity score.

    Returns:
    Tuple[float, str]: a tuple containing the average polarity as a float and the corresponding color as a string.
    """
    total_polarity = sum(review.get('textblob_polarity', 0) for review in reviews)
    average_polarity = total_polarity / len(reviews) if reviews else 0

    # Determine the color based on average polarity
    if average_polarity < -0.25:
        color = "red"  # Red light for negative sentiment
    elif average_polarity > 0.25:
        color = "green"  # Green light for positive sentiment
    else:
        color = "orange"  # Orange light for neutral sentiment

    return average_polarity, color

# Create function to display average polarity and corresponding colored circle
def display_average_polarity_and_color() -> None:
    """
    The function displays the average polarity of all reviews and represents it with a colored circle:
    a green circle represents a positive average polarity, red indicates negative, and orange is for
    neutral sentiment. If no reviews are available, it updates the GUI to indicate this.

    Arguments:
    None: the function uses global variables to access the data it needs.

    Returns:
    None: this function does not return any value. It updates the GUI directly.
    """
    if all_results:
        average_polarity, color = get_polarity_color(all_results)
        polarity_text = f"Average Polarity Score: {average_polarity:.2f}"
        polarity_label.config(text=polarity_text)  # Update label text
        polarity_canvas.delete("all")  # Clear previous circle
        polarity_canvas.create_oval(5, 5, 40, 40, fill=color, outline=color)  # Draw circle
    else:
        polarity_label.config(text="No reviews available to calculate average polarity.")
        polarity_canvas.delete("all")  # Clear the canvas

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

# Create a function to allow selection of a product among the ones retrieved
def on_select(event: tk.Event) -> None:

    """
    On selection of a row of the treeview widget.

    Arguments:
    event (Tkinter Event): the event object triggered by the Treeview selection.

    Returns:
    None: prints the selected URL and assigns it to the global variable 'selection_url'.
    """
    global product_id
    global product_url

    selected_items = products_tree.selection()
    # to prevent error message 
    if selected_items:
        selected_item = selected_items[0]
    else:
        print("No item selected")

    selected_index = products_tree.index(selected_item)
    product_id = product_df.loc[selected_index, 'ASIN']
    product_url = product_df.loc[selected_index, 'Product URL']

    product_text_scrape = scrape_amazon_product_description(product_url)

    product_text.delete(1.0, tk.END)
    if product_text_scrape:
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
    keyword (str): the search keyword inserted by the user.
    search_param (str): the search parameter (e.g., 'Books', 'Electronics') which is equivalent to the Amazon homepage.
    num_pages (int): the number of pages to scrape (default is 1 to not pulling to many requests and get blocked).

    Returns:
    None: creates treeview table and saves results in the csv file "amazon_product_data.csv".
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
            products_tree.insert("", "end", values=(i + 1, row["Product Name"], row["ASIN"]))

        # Save DataFrame to CSV
        product_df.to_csv('amazon_product_data.csv', index=False)

def open_amazon():
    webbrowser.open_new(product_url)

# Initialize the main application window using Tkinter
app = tk.Tk()
app.title("Amazon Review Analyzer")  
app.geometry("3024x1964")

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
tk.Label(left_frame, text="Keyword:").grid(row=0, column=0, padx=110, pady=20, sticky="w")
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
    values=list(search_params.values()), 
    state='readonly'  # Set the Combobox state to readonly
)
search_param_dropdown.set(list(search_params.values())[0])
search_param_dropdown.grid(row=1, column=1, pady=5, sticky="w")

# Create entry to set the number of pages
num_pages_entry = tk.Entry(left_frame, width=5)
num_pages_entry.grid(row=2, column=1, pady=5, sticky="w")

# Set default value to 1
num_pages_entry.insert(0, "1")

# Create button to start the search
search_button = tk.Button(left_frame, text="Search Amazon", command=lambda: update_treeview(keyword_entry.get(), value_to_key(search_param_var.get()), int(num_pages_entry.get())))
search_button.grid(row=3, column=0, columnspan=2, padx=300, pady=20, sticky="w")

# Returns the key for the value of the search_params dictionary - to sort out the problem that the value should be display in the dropdown but the key used for the search
def value_to_key(search_value: str) -> Optional[str]:
    """
    Returns the key corresponding to the given value from the 'search_params' dictionary.

    Arguments:
    search_value (str): the value for which the corresponding key is to be returned.

    Returns:
    Optional[str]: the key corresponding to the provided value. If the value is not found, returns None.
    """
    for key, value in search_params.items():
        if value == search_value:
            return key
    return None  # Return None if the value is not found

# Treeview to display the product list - the search result 
products_tree = ttk.Treeview(left_frame, columns=("Number", "Product Name", "ASIN"), show="headings")
products_tree.heading("Number", text="Number")
products_tree.heading("Product Name", text="Product Name")
products_tree.heading("ASIN", text="ASIN")
products_tree.grid(row=4, column=0, columnspan=2, padx=15, pady=15, sticky="w")

# Configure the column widths
products_tree.column("Number", width=100, anchor='center')
products_tree.column("Product Name", width=445, anchor='w')
products_tree.column("ASIN", width=140, anchor='w')

# Bind the on_select function to the Treeview's selection event - when a product is actually selected 
products_tree.bind("<<TreeviewSelect>>", on_select)

# Create a label for the Product Description field
product_text_label = tk.Label(left_frame, text="Product Description:")
product_text_label.grid(row=5, column=0, padx=15, pady=5, sticky="w")

# Create a text field for displaying the Product Description
product_text = tk.Text(left_frame, wrap=tk.WORD, height=8, width=85, font=sf_pro_font)  
product_text.grid(row=6, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Create a button to go to the selected Amazon product homepage 
go_to_amazon_button = tk.Button(left_frame, text="Go to Amazon", command=open_amazon)
go_to_amazon_button.grid(row=7, column=0, columnspan=2, padx=320, pady=5, sticky="w")

# Label and entry for number of review pages
tk.Label(right_frame, text="Number of Review Pages:").grid(row=1, column=0, pady=20, sticky="e")
review_pages_entry = tk.Entry(right_frame, width=5)
review_pages_entry.grid(row=1, column=1, padx=1, pady=20, sticky="w")

# Set default value to 1
review_pages_entry.insert(0, "1")

# Create a button that, when clicked, will start the scraping process
scrape_button = tk.Button(right_frame, text="Scrape Reviews", command=start_scraping_thread, state=tk.DISABLED)
scrape_button.grid(row=1, column=1, padx=106, pady=20, sticky="w")

# Create a text area where the scraped review data will be displayed
text_area = tk.Text(right_frame, wrap=tk.WORD, width=85, height=10, font=sf_pro_font)
text_area.grid(row=2, column=0, columnspan=2, padx=15, pady=3, sticky="w")

# Frame for the subjectivity filters
subjectivity_frame = tk.Frame(right_frame)
subjectivity_frame.grid(row=3, column=0, columnspan=1, pady=(5, 5), sticky='ew')
min_subjectivity_label = tk.Label(subjectivity_frame, text="Min Subjectivity (0 to 1):", font=tkFont.Font(size=9))
min_subjectivity_label.grid(row=0, column=0, padx=20, pady=2, sticky='w')
min_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
min_subjectivity_entry.grid(row=0, column=1, padx=5, pady=2, sticky='w')

max_subjectivity_label = tk.Label(subjectivity_frame, text="Max Subjectivity (0 to 1):", font=tkFont.Font(size=9))
max_subjectivity_label.grid(row=1, column=0, padx=20, pady=2, sticky='w')
max_subjectivity_entry = tk.Entry(subjectivity_frame, width=5)
max_subjectivity_entry.grid(row=1, column=1, padx=5, pady=2, sticky='w')

# Subjectivity explanation 
subjectivity_explanation_text = (
    "Subjectivity score measures how subjective or opinionated the review is,\n"
    "and ranges from 0 (completely objective) to 1 (completely subjective)."
)
subjectivity_explanation = tk.Label(right_frame, text=subjectivity_explanation_text, font=tkFont.Font(size=9), justify="left")
subjectivity_explanation.grid(row=3, column=1, padx=1, pady=1, sticky='w')

# Frame for the polarity filters
polarity_frame = tk.Frame(right_frame)
polarity_frame.grid(row=4, column=0, columnspan=1, pady=(5, 5), sticky='ew')
min_polarity_label = tk.Label(polarity_frame, text="Min Polarity (-1 to 1):", font=tkFont.Font(size=9))
min_polarity_label.grid(row=0, column=0, padx=20, pady=2, sticky='w')
min_polarity_entry = tk.Entry(polarity_frame, width=5)
min_polarity_entry.grid(row=0, column=1, padx=5, pady=2, sticky='w')

max_polarity_label = tk.Label(polarity_frame, text="Max Polarity (-1 to 1):", font=tkFont.Font(size=9))
max_polarity_label.grid(row=1, column=0, padx=20, pady=2, sticky='w')
max_polarity_entry = tk.Entry(polarity_frame, width=5)
max_polarity_entry.grid(row=1, column=1, padx=5, pady=2, sticky='w')


# Polarity explanation
polarity_explanation_text = (
    "Polarity score measures how negative or positive the sentiment of the review is,\n"
    "and ranges from -1 (extremely negative) to 1 (extremely positive)."
)
polarity_explanation = tk.Label(right_frame, text=polarity_explanation_text, font=tkFont.Font(size=9), justify="left")
polarity_explanation.grid(row=4, column=1, padx=1, pady=1, sticky='w')

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
wordcloud_button = tk.Button(right_frame, text="Show Word Cloud", command=display_wordcloud)
wordcloud_button.grid(row=11, column=0, columnspan=2, padx=300, pady=5, sticky="w")

# Start the application's main event loop, ready for user interaction
app.mainloop()