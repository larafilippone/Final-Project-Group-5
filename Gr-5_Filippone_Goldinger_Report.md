# Extracting Sentiment and Insights from Amazon Reviews to Improve Products

**Introduction to Computer Science and Programming**

Lara Filippone, Florian Goldinger

25.01.2024

## Introduction
In the ever-evolving domain of e-commerce, customer experience and feedback have become more and more significant. Recognizing the central role of these dimensions for businesses, our project aimed to explore the potential of modern technology to optimize and innovate the processing of customer opinions. Specifically, we focused on Amazon product reviews, a rich source of consumer insights, although generally difficult to fully explore due to its great volume and unstructured nature.

The primary objective of this project was the development of the Amazon Review Analyzer, an analytical tool tailored for customer service, product managers and Amazon sellers in general. Our proposal is designed to facilitate and automate the analysis of extensive textual data from Amazon product reviews. By doing so, it empowers these stakeholders to gain instant insights on customer sentiments, experiences, and preferences, leading to informed decision-making and product enhancements.

To achieve this, we outlined the following key functionalities for our application:

**Collection of Amazon reviews**: employing web scraping techniques, the tool can gather reviews for a specific product from Amazon. This forms the foundational dataset for subsequent analyses.

**Sentiment analysis**: the tool performs sentiment analysis on the collected reviews, assigning a numerical score according to their positive, negative, or neutral content. This provides a quantitative measure of customer satisfaction that can be later employed for further analysis.

**Keyword identification**: by analyzing the review text, the tool identifies recurring keywords, highlighting the most discussed aspects of the product.

**Generative AI for summarization**: through the use of generative AI, the tool synthesizes the vast amount of review data into concise summaries. These summaries offer automated and quick insights into the overall customer experience.

**Generative AI for product improvement suggestions**: additionally, the tool uses generative AI to automatically propose actionable product improvements based on the review analysis.

**User-friendly GUI**: to ensure accessibility and ease of use, said functionalities are condensed within an intuitive and user-friendly Graphical User Interface (GUI) and accompanied by meaningful and evocative visualizations.

The expected outcome of this project was the implementation of a tool that showcases the potential of integrating various functionalities into a single platform. Although our tool is a preliminary and simple version, it is thought as a proposal for how such a system could be developed and utilized in a real-world scenario. By demonstrating the feasibility and effectiveness of combining web scraping, sentiment analysis, keyword identification, and generative AI technologies for the analysis of Amazon product reviews, this project offers insights into the practical applications of these technologies in e-commerce and customer feedback analysis.

## Code Quality and Functionality

### Code Overview
In developing our Amazon Review Analyzer application, we employed a range of tools:

The Integrated Development Environment (IDE) used was **Visual Studio Code**, primarily for the possibility of creating and managing virtual environments. This feature was particularly important in the development of our application, as it allowed us to isolate of project-specific dependencies, ensuring a clean and controlled development workspace.

The core programming language used to develop our application was **Python**, specifically version 3.11.5. We opted for this version instead of newer ones to ensure compatibility with all the libraries used in our project.

To implement the web scraping functionalities, one of the central aspects of the application, we employed **BeautifulSoup**. This library is particularly suitable for parsing HTML and XML documents, making it ideal for extracting data from Amazon's complex web pages.

For sentiment analysis, we incorporated the **TextBlob** library, which represents a great choice to easily analyze the textual content of Amazon reviews.

Our application additionally integrates the **OpenAI API** to connect with the advanced natural language processing abilities of ChatGPT. This integration enables the application to generate insightful summaries and suggestions based on the Amazon product reviews.

For the GUI development, we relied on **Tkinter**, a standard GUI toolkit in Python that offers the possibility to easily create intuitive and user-friendly interfaces.

Our project's codebase was divided into multiple scripts to ensure readability, maintainability, and reusability. The scripts were organized as follows:

`main.py`: the main Python script and the entry point of the application. It sets up the main GUI layout using Tkinter and handles the orchestration and event processing between different components.

`scraping_utils.py`: this script contains functions and utilities for the web scraping processes, primarily using BeautifulSoup to scrape data from Amazon.

`data_analysis.py`: dedicated to analyzing the extracted data from Amazon reviews, this script contains the functions related to sentiment analysis and keyword identification.

`chatgpt_integration.py`: this script manages the integration with the ChatGPT API.

`utils.py`: a collection of general utility functions used throughout the application for code reusability and consistency.

`config.py`: the script containing configuration settings and constants, defining important parameters for easy configuration of the application.

### Code functionality and quality

In the following, we will walk through the main scripts described above and explain important code snippets. This section covers only the key code segments. Further details can be obtained in the scripts where everything has been commented out in detail. Docstrings are added to all of the functions to explain the purpose of the function, the arguments and what is returned. 

#### main.py

The `main.py` script serves as the entry point of the application. Its primary functions include generating the Graphical User Interface (GUI) and managing the interaction among different features.

The script begins by importing essential packages needed in later stages, such as `WordCloud` and `matplotlib`. Within the project's virtual environment, these packages must be installed using pip install. All the requirements are listed in the requirements.txt file.

In addition to the public packages, this section of the code imports custom functions created for the project, such as `scrape_data` and `ask_chatgpt`. These functions are organized into modules containing functions with similar functionality. This approach enhances code readability and promotes code reuse.

``` python
...
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

from chatgpt_integration import ask_chatgpt
from config import SEARCH_PARAMS
from data_analysis import get_polarity_color, generate_filtered_text
from scraping_utils import get_amazon_product_data, scrape_amazon_product_description, scrape_data
...
```
The graphical user interface is initialized in the main script by using the Tkinter library. `app = tk.Tk()` creates the window that can later be populated with different widgets. The window size is dynamically adapted to the size of the computer screen. 

``` python 
# Initialize the main application window using Tkinter
app = tk.Tk()
app.title("Amazon Review Analyzer")
```
To achieve a well-organized layout, the window was divided into two separate frames. These frames serve as invisible containers for placing widgets, and a row-and-column grid system was employed for precise widget placement within these frames.
 
 ``` python
 # Create frames for the left and right sides
left_frame = tk.Frame(app, borderwidth=0, relief="flat")
right_frame = tk.Frame(app, borderwidth=0, relief="flat")
```

Exemplary, below you can find the placement of a button widget to start the search process and update the treeview (table) widget. 

``` python
# Create button to start the search
search_button = tk.Button(
    left_frame,
    text="Search Amazon",
    command=lambda: update_treeview(
        keyword_entry.get(), value_to_key(search_param_var.get()), int(num_pages_entry.get())
    ),
)
search_button.grid(row=3, column=0, columnspan=2, padx=300, pady=20, sticky="w")
```
The button is positioned within the links_frame using the grid layout. The parameters in the grid method determine the row, column, and the padding (distance) with respect to the x and y axes. With the command attribute, the function starting the scraping process `update_treeview` is linked to the button and executed when the user clicks on it. The `update_treeeview` function takes on the values entered into the keyword, search_param and num_pages field as attributes. 

Thus a click starts this function: 

``` python
def update_treeview(keyword: str, search_param: str, num_pages: int) -> None:
...
    product_df = pd.DataFrame(columns=["Number", "Product Name", "Product URL", "ASIN"])
    product_data = get_amazon_product_data(keyword, search_param, num_pages)
    product_df = pd.concat([product_df, pd.DataFrame(product_data)], ignore_index=True)

    for row in products_tree.get_children():
        products_tree.delete(row)

    if not product_df.empty:
        for i, row in product_df.iterrows():
            products_tree.insert("", "end", values=(i + 1, row["Product Name"], row["ASIN"]))
```
This function again enters the values received from the function `get_amazon_product_data` into the Dataframe `product_df`and updates the treeview widget with the same data and the command `products_tree.insert`.

Similarily other widgets are linked to imported functions that execute scraping processes or for example access the Chat GPT API. 

Thus the button for scraping, on selection executes the following functions consecutively: 

- `scrape_data(product_id, num_review_pages)` scrapes all the reviews of a specific product_id
- `display_review(review)` displays the reviews in a text field 
- `display_average_polarity_and_color()` displays the average polarity in a graphic (red, orange, green)
- `display_chatgpt(all_results)` connects to ChatGPT and displays results in two text fields 

Thus the GUI is built up in the main script, retrieving information from the user like the product searched and on selection of buttons or lists is executing functions of imported modules. These functions again are executing scraping processes, further processing the data or displaying information.

The Tkinter code is framed with the command ```app.mainloop()``` which starts the main event loop of the Tkinter application. This loop listens for events such as button clicks, product selection, etc., and it keeps the application running. It is placed at the end of the Tkinter script, after we have defined all our GUI components. 

``` python
# Start the main event loop
app.mainloop()
```
#### scraping_utils.py

The module `scraping_utils.py` contains all the functions related to the scraping of online content from Amazon. Their implementation mainly relies on the BeatifulSoup library. Here we will discuss three key functions: `get_page_html`, `get_reviews_from_html`, and `get_review_text`.

The `get_page_html` function is responsible for retrieving the HTML content of a web page. This function initializes the scraping process. It employs the requests library to send a GET request to the specified page URL, and returns the HTML content of the page.

``` python
# Create a function to retrieve the HTML code of a web page
def get_page_html(page_url: str) -> str:
    try:
        # Choose a random user agent
        user_agent = random.choice(USER_AGENTS)
        # Update the 'user-agent' in the HEADERS
        HEADERS["user-agent"] = user_agent

        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return ""  # Return empty string in case of an error
```
An important feature of this function is its use of random user agents from a predefined list (`USER_AGENTS`). This is a precaution taken to prevent detection as a bot by the website’s security systems.

Once the HTML content is retrieved, `get_reviews_from_html` continues the process: it parses the HTML using BeautifulSoup and extracts the review elements. This function is essential for isolating the specific data (reviews) we are interested in from the entire HTML code.
``` python
# Create a function to retrieve review elements from HTML code
def get_reviews_from_html(page_html: str) -> list:
    soup = BeautifulSoup(page_html, "lxml")

    # Try finding review elements by 'data-hook' attribute with value 'review'
    reviews = soup.find_all("div", attrs={"data-hook": "review"})

    # If no reviews are found with the 'data-hook' attribute, try different classes
    if not reviews:
        reviews = soup.find_all("div", class_="a-section celwidget")

    return reviews
```
The function uses BeautifulSoup's parsing functionalities to locate review elements, first trying to find them by a specific 'data-hook' attribute and then by a class name. This dual approach ensures that the detection works for every product, considering the variability in Amazon’s page structure.

The `get_review_text function` is an example of how specific pieces of information are extracted from each review. Similar functions are used for retrieving other parts of a review, namely the title, the date and the rating.
``` python
# Create a function to retrieve the review text
def get_review_text(soup_object: BeautifulSoup) -> str:
    review_text = soup_object.find("span", {"class": "a-size-base review-text review-text-content"})
    # If the class selector doesn't find the element, try the data-hook attribute
    if not review_text:
        review_text = soup_object.find("span", {"data-hook": "review-body"})

    return str(review_text.get_text().strip()) if review_text else "No review text"
```
This function demonstrates our approach to handling variability in HTML structures: it first attempts to find the review text using one class selector and, if unsuccessful, it tries another selector. Again, the different attempts ensure that the data extraction works with differently structured Amazon web pages.

#### data_analysis.py

The `data_analysis.py` module provides functionalities for analyzing and visualizing data extracted from Amazon reviews. It includes three significant functions: `analyze_sentiment_with_textblob`, `get_polarity_color`, and `generate_filtered_text`.

The `analyze_sentiment_with_textblob` function is designed to perform sentiment analysis on the given text. It utilizes the TextBlob library, suited for natural language processing tasks.
``` python
# Create a function to perform sentiment analysis
def analyze_sentiment_with_textblob(text: str):
    testimonial = TextBlob(text)
    return testimonial.sentiment
```
This function takes a string input (the review text) and returns the sentiment analysis result, which includes polarity and subjectivity scores. Polarity measures how positive or negative the text is, while subjectivity measures how subjective or opinionated the text is.

The `get_polarity_color` function calculates the average polarity score of all reviews and outputs a corresponding color based on the score.

``` python
# Create function to calculate average polarity score and output corresponding color
def get_polarity_color(reviews: List[Dict[str, Any]]) -> Tuple[float, str]:
    total_polarity = sum(review.get("textblob_polarity", 0) for review in reviews)
    average_polarity = total_polarity / len(reviews) if reviews else 0

    # Determine the color based on average polarity
    if average_polarity < -0.25:
        color = "red"  # Red light for negative sentiment
    elif average_polarity > 0.25:
        color = "green"  # Green light for positive sentiment
    else:
        color = "orange"  # Orange light for neutral sentiment

    return average_polarity, color
```
The function iterates through a list of reviews, sums up their polarity scores, and calculates the average. Based on this average, it assigns a color: red for negative sentiment, green for positive, and orange for neutral. This color-coding system provides a quick and intuitive way to assess the general sentiment of the reviews.

The `generate_filtered_text` function preprocesses review texts for creating a word cloud. This involves tokenizing the text, removing common English stopwords, and filtering out non-alphabetical characters.
``` python
# Create a function to preprocess text for the word cloud
def generate_filtered_text(all_results: List[Dict[str, Any]]) -> str:
    if not all_results:
        return ""

    # Combine all review texts into a single string
    text = " ".join(review["review_text"] for review in all_results)

    # Tokenize the text and remove stopwords
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    return " ".join(word for word in words if word.lower() not in stop_words and word.isalpha())
```
The function creates a concatenated string of all important words from the reviews, which can then be used to generate a word cloud.

#### chatgpt_integration.py

The module `chatgpt_integration.py` is providing the functions to interact with the OpenAI API. After setting up an account with OpenAI a personal access token will be generated that can be used to access the API `openai.api_key = "xx"`. The token is not stored in the script as we work with a public Git repository and we don't want to publish it. The token has to be added manually. In a more extensive project a shell script could be included to add on the key token that is stored locally. 

``` python
        # Insert the key for Open AI
        openai.api_key = "xx"

        # Accesses the API of Chat GPT to ask the question_to_chatgpt generated earlier
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an informative assistant."},
                {"role": "user", "content": question_to_chatgpt},
            ],
            temperature=0.7,
        )

        # Save and return the generated content
        generated_content = response["choices"][0]["message"]["content"]

        return str(generated_content.strip())
```

When accessed, the API allows to generate an answer with the function `openai.ChatCompletion.create()`. The appropriate question to ChatGPT has been created earlier and stored in the variable `question_to_chatgpt`. 
In general, we ask ChatGPT questions in a manner similar to how one would use the online tool. This has shown to generate the best responses. For the summary we ask "Summarize the negative and positive sentiment of the reviews attached. Limit to 6 bullet points."

With the message attribute we can specify how the answer should look like in general and that the content should be informative. The temperature attribute indicates on how "creative" the answer should be. We limited to 0.7 which indicates moderate randomness.  

The answer can be accessed by `response["choices"][0]["message"]["content"]`. As ChatGPT generates several answers, with choice = 0 and message = content, the content of the first answer is accessed and then returned after making sure that it is in string format. 

*Error Handling*

As to all the scripts where we interact with a web server or with an API we have added on error handling. Because in such situations we might face runtime errors. As such we can detect them and inform accordingly.

``` python
try:
...
except openai.error.AuthenticationError as e:
    print(f"OpenAI API error: {e}")
    return "Authentication error: please check your Chat GPT API key"
except ValueError as ve:
    print(f"Value error: {ve}")
    return "A value error occurred while processing your request."
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
    return "An unexpected error occurred while processing your request."
```

In the case of ChatGPT, we want to emphasize the first 'except' command, specifically except `openai.error.AuthenticationError as e:`, which identifies authentication problems. This may occur if you forget to manually add a correct API key token. In such cases, an error message is printed, prompting you to enter a valid key in the GUI.


### Testing and Bug-Fixing
In the development of our application, we employed a series of testing tools and methodologies to ensure code quality and functionality. These included:

**Mypy**: A static type checker for Python, used to detect type errors in our code, to ensure that the types of variables and returned values are correctly implemented.
*Black*: An automatic code formatter for Python, making sure to adhere to a consistent style and format, essential for readability and maintainability.

**Pylint**: A Python static code analysis tool, used to identify coding errors, enforce a coding standard, and look for code smells, which helped in maintaining high-quality code.

**isort**: A Python library to sort imports alphabetically, and automatically separate them into sections. It made our import statements more organized and readable.

**unittest**: The built-in Python unit testing framework was utilized to create and run tests on individual functions. Each module in our project has a corresponding "*_test.py" file within the "tests" folder in our repository, where we conducted the necessary testing of the functions contained in each module. However, it is important to note that tests did not include some functions linked to GUI commands or elements, as these were more effectively tested directly within the GUI environment.

This testing approach ensured that our code was not only functional but also adhered to best practices in terms of style and structure.

As far as bug-fixing is concerned, during the development process we encountered a significant challenge related to the variability in Amazon's page structure, which affected the correct functioning of our scraping functions. Specifically, our scraping functions as we initially implemented them were not able to consistently scrape the desired elements from the product pages, as Amazon's page layouts can vary greatly from product to product.

To address this issue, we adopted an iterative and hands-on approach: initially, we tested our application with a wide range of products to identify where the scraping functions were failing. Afterwards, we accurately inspected the HTML structure of the problematic product pages. This way, we could understand how the coding patterns differed from our initial expectations.
Based on the insights gained from these inspections, we adapted our scraping functions to be more versatile.

This adaptation process was particularly challenging for functions like `scrape_amazon_product_description`: to cope with the diverse structures of Amazon product pages, we had to implement a series of conditional checks to identify different HTML elements that could contain the product description. The final function first attempts to find the description in one HTML structure, and if unsuccessful, it moves on to check for alternative structures. Each of these approaches contained within the function represents a different strategy for locating and extracting the product description, depending on the specific layout of the Amazon page.

## Collaboration and Teamwork

We decided to split our tool into distinct features, allowing each team member to work on specific parts of the project. Overall, we managed to achieve a good and equal distribution of the total workload.

We identified the following sub-features with the corresponding person in charge:

1. **Amazon Search Feature** (Florian): Replicating the search functionality as known from the Amazon homepage. This involved analyzing the functioning of the Amazon search, examining the HTML code of the landing pages, developing scraping techniques, extracting ASIN for other features, and displaying the results in the GUI.

2. **Product Description** (Florian): Following the product search, upon selecting a product, the product description should be shown. Again, Amazon landing pages are diverse, requiring different scraping approaches for the various versions and associated HTML source code.

3. **Scraping Amazon Reviews** (Lara): Developing different scraping versions based on the HTML source code, which varies across different product pages.

4. **Sentiment Analysis** (Lara): Deploying sentiment analysis on the reviews, displaying both subjectivity and polarity scores.

5. **Filter Feature** (Lara): Enhancing the display of sentiment results by introducing a filter based on subjectivity and polarity.

6. **Graphical Display of Sentiment** (Lara): Introducing a graphical display (red, orange, green) based on the average sentiment score.

7. **Chat GPT API** (Florian): Connecting the tool with Chat GPT, developing the correct connection through the API.

8. **Product Summary / Improvement** (Florian): Gathering and displaying the product summary and improvement suggestions using the Chat GPT API.

9. **Graphical Wordcloud** (Lara): Implementing a word cloud display that summarizes key words in the reviews. Stop words had to be filtered out to obtain an appropriate result.

10. **Integration of Features** (team): Integrating all features into a seamless, logical process and into one main script.

11. **Graphical User Interface** (team): Developing a user-friendly and intuitive interface to easily use the tool and display all relevant results in a summarized way.

12. **Testing** (team): Extensive testing of the code and the GUI. 

13. **Code Improvement / Bug Fixing** (team): Using various tools (Pylint, Mypy, Black, isort, unittest) to improve the code and fix bugs.

### Collaboration techniques

Overall, we managed to foster a strong team spirit in which both team members could contribute equally to the project. We developed a supportive mindset, collaborating on each other's features and working together to find overall solutions. Consequently, we could easily integrate all the different parts of the project.

The main tool we used for the code part was **GitHub**. It was essential for a project of this scope to correctly version control the code and integrate all parts of the project. In summary, it wouldn't have been possible to work without it.

To discuss the project architecture and communicate progress, we set up regular in-person **meetings** at the University, but we also utilized **Zoom** calls. For quick updates, we used **WhatsApp**. As both team members were responsive, we could maintain a constant exchange, and everyone stayed up to date.

### Conflict resolution

No real conflicts arose as we communicated effectively and both were motivated to develop a good tool. The main reasons for the smooth process were a well-defined project scope (architecture), division of feature development tasks, and consistent updates to keep each other informed. 

## Project Design and Creativity

### Innovation and Creativity
Our project introduces an innovative solution intended for sellers, customer service, and product management teams who often encounter the challenge of managing an overwhelming quantity of product reviews. One of the key features of our application is its ability to filter reviews based on sentiment, moving beyond the traditional star rating system. This functionality allows for a more insightful understanding of customer feedback.

The integration with ChatGPT represents another innovative aspect, as it enables the app to provide immediate, AI-driven insights into the key aspects highlighted in positive and negative reviews, along with suggestions for product improvement, based on the insights retrieved from customer complaints. This can significantly accelerate the process of addressing customer service issues and adapting products to meet customer needs and preferences, providing sellers with a rapid and clear understanding of their products' reception.

Our application includes creative solutions as well, like the generation of word clouds from review keywords. This functionality creates an engaging visual representation of the most discussed topics, and besides adding a visual appeal it can also serve a practical purpose in presentations, making the data both impactful and straightforward.

Moreover, we make use of color coding to represent the average sentiment polarity of the reviews: green for positive, orange for neutral, and red for negative sentiments. This intuitive use of colors creates an immediate, evocative understanding of the overall sentiment, enhancing the impact and interpretability of the data.

### User Experience
As far as user experience is concerned, our tool is designed to be user-friendly and accessible: despite the complexity of the underlying Python code, users can directly interact with a simple and intuitive GUI. Precisely, the interface mimics the familiar experience of browsing the Amazon website, allowing users to input a product name, keyword, or ASIN to receive a list of results in a straightforward format.

The GUI also includes explanatory notes on polarity and subjectivity scores, clearly informing users about what these metrics mean and how they can be interpreted. All other widgets and functionalities within the GUI are designed to be straightforward and self-explanatory, meaning that users can benefit from the sophisticated analysis our tool provides without the need to have a technical background.

## Conclusion

In conclusion, our efforts have resulted in the successful development of the **Amazon Review Analyzer** application, covering the defined key features such as web scraping, automated sentiment analysis, and the generation of insightful summaries and improvement suggestions based on customer reviews. 

Throughout this project, we not only achieved our technical objectives but also gained important learnings from the development process. It was a crucial learning outcome in understanding how to work together, manage different aspects of the project, and seamlessly integrate everything into one product. This involved thorough testing, improving the tool, and bug fixing. For us the experience highlighted the importance of teamwork and effective communication. We also learned on how to use tools like GitHub to help us achieve this. 

Our exploration of techniques, including complex web scraping and the integration of tools through APIs, has also broadened our understanding of practical applications of these technologies.

The acquired knowledge and skills hopefully lay the groundwork for future projects, where we can delve deeper into these techniques and explore additional real-world applications. We can think about numerous potential projects where we could deepen our knowledge and apply these capabilities. 

We are happy with the outcomes, learning new skills and successfully achieving the goals we initially set.



## References
Jeff James. (2019). "amazon_review_scraper.py". GitHub gist. https://gist.github.com/jrjames83/4653d488801be6f0683b91eda8eeb627

Leonard Richardson. (2023). Beautiful Soup Documentation. https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Python Software Foundation. (2023). Tkinter — Python interface to Tcl/Tk. https://docs.python.org/3/library/tkinter.html

Python Software Foundation. (2023). unittest — Unit testing framework. https://docs.python.org/3/library/unittest.html

Steven Loria and Contributors. (2023). TextBlob: Simplified Text Processing. https://textblob.readthedocs.io/

The Black Contributors. (2023). Black: The uncompromising code formatter. https://black.readthedocs.io/en/stable/

The isort Contributors. (2023). isort: A Python utility/library to sort imports. https://pycqa.github.io/isort/

The Mypy Contributors. (2023). Mypy: Optional Static Typing for Python. https://mypy.readthedocs.io/

The Pylint Contributors. (2023). Pylint - code analysis for Python. https://pylint.pycqa.org/