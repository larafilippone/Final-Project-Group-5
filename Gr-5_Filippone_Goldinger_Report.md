# Extracting Sentiment and Insights from Amazon Reviews to Improve Products

### Introduction to Computer Science and Programming

Lara Filippone, Florian Goldinger

25.01.2024

## Introduction
In the ever-evolving domain of e-commerce, customer experience and feedback have become more and more significant. Recognizing the central role of these dimensions for businesses, our project aimed to explore the potential of modern technology to optimize and innovate the processing of customer opinions. Specifically, we focused on Amazon product reviews, a rich source of consumer insights, although generally difficult to fully explore due to its great volume and unstructured nature.

The primary objective of this project was the development of the Amazon Review Analyzer, an analytical tool tailored for customer service, product managers and Amazon sellers in general. Our proposal is designed to facilitate and automate the analysis of extensive textual data from Amazon product reviews. By doing so, it empowers these stakeholders to gain instant insights on customer sentiments, experiences, and preferences, leading to informed decision-making and product enhancements.

To achieve this, we outlined the following key functionalities for our application:

Collection of Amazon reviews: employing web scraping techniques, the tool can gather reviews for a specific product from Amazon. This forms the foundational dataset for subsequent analyses.

Sentiment analysis: the tool performs sentiment analysis on the collected reviews, assigning a numerical score according to their positive, negative, or neutral content. This provides a quantitative measure of customer satisfaction that can be later employed for further analysis.

Keyword identification: by analyzing the review text, the tool identifies recurring keywords, highlighting the most discussed aspects of the product.

Generative AI for summarization: through the use of generative AI, the tool synthesizes the vast amount of review data into concise summaries. These summaries offer automated and quick insights into the overall customer experience.

Generative AI for product improvement suggestions: additionally, the tool uses generative AI to automatically propose actionable product improvements based on the review analysis.

User-friendly GUI: to ensure accessibility and ease of use, said functionalities are condensed within an intuitive and user-friendly Graphical User Interface (GUI) and accompanied by meaningful and evocative visualizations.

The expected outcome of this project was the implementation of a tool that showcases the potential of integrating various functionalities into a single platform. Although our tool is a preliminary and simple version, it is thought as a proposal for how such a system could be developed and utilized in a real-world scenario. By demonstrating the feasibility and effectiveness of combining web scraping, sentiment analysis, keyword identification, and generative AI technologies for the analysis of Amazon product reviews, this project offers insights into the practical applications of these technologies in e-commerce and customer feedback analysis.

## Code Quality and Functionality

### Code overview
In developing our Amazon Review Analyzer application, we employed a range of tools:

The Integrated Development Environment (IDE) used was Visual Studio Code, primarily for the possibility of creating and managing virtual environments. This feature was particularly important in the development of our application, as it allowed us to isolate of project-specific dependencies, ensuring a clean and controlled development workspace.

The core programming language used to develop our application was Python, specifically version 3.11.5. We opted for this version instead of newer ones to ensure compatibility with all the libraries used in our project.

To implement the web scraping functionalities, one of the central aspects of the application, we employed BeautifulSoup. This library is particularly suitable for parsing HTML and XML documents, making it ideal for extracting data from Amazon's complex web pages.

For sentiment analysis, we incorporated the TextBlob library, which represents a great choice to easily analyze the textual content of Amazon reviews.

Our application additionally integrates the OpenAI API to connect with the advanced natural language processing abilities of ChatGPT. This integration enables the application to generate insightful summaries and suggestions based on the Amazon product reviews.

For the GUI development, we relied on Tkinter, a standard GUI toolkit in Python that offers the possibility to easily create intuitive and user-friendly interfaces.

Our project's codebase was divided into multiple scripts to ensure readability, maintainability, and reusability. The scripts were organized as follows:

main.py: the main Python script and the entry point of the application. It sets up the main GUI layout using Tkinter and handles the orchestration and event processing between different components.

scraping_utils.py: this script contains functions and utilities for the web scraping processes, primarily using BeautifulSoup to scrape data from Amazon.

data_analysis.py: dedicated to analyzing the extracted data from Amazon reviews, this script contains the functions related to sentiment analysis and keyword identification.

chatgpt_integration.py: this script manages the integration with the ChatGPT API.

utils.py: a collection of general utility functions used throughout the application for code reusability and consistency.

config.py: the script containing configuration settings and constants, defining important parameters for easy configuration of the application.


Test code snippet:

``` python
product_description_div = soup.find("div", {"id": "productFactsDesktopExpander"})

    if product_description_div:
        # Check for several unordered lists betwen <ul class="a-unordered-list a-vertical a-spacing-small"> and </ul>
        unordered_lists = product_description_div.find_all("ul", {"class": "a-unordered-list"})

        if unordered_lists:
            description_text = ""

            for ul in unordered_lists:
                # Find all list items within the unordered list
                item_list = ul.find_all("li")

                if item_list:
                    # Extract text from each list item
                    list_text = "\n".join(
                       "/ " + item.find("span", {"class": "a-list-item"}).text.strip() for item in item_list
                        )

                        # Append the list text to the overall description
                        description_text += list_text

                print("version 2")
                return description_text.strip()
```

### Code functionality and quality

### Testing and bug-fixing

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

13. **Code Improvement / Bug Fixing** (team): Using various tools (pylint, mypy, black) to improve the code and fix bugs.

### Collaboration techniques

Overall, we managed to foster a strong team spirit in which both team members could contribute equally to the project. We developed a supportive mindset, collaborating on each other's features and working together to find overall solutions. Consequently, we could easily integrate all the different parts of the project.

The main tool we used for the code part was **GitHub**. It was essential for a project of this scope to correctly version control the code and integrate all parts of the project. In summary, it wouldn't have been possible to work without it.

To discuss the project architecture and communicate progress, we set up regular in-person **meetings** at the University, but we also utilized **Zoom** calls. For quick updates, we used **WhatsApp**. As both team members were responsive, we could maintain a constant exchange, and everyone stayed up to date.

### Conflict resolution

No real conflicts arose as we communicated effectively and both were motivated to develop a good tool. The main reasons for the smooth process were a well-defined project scope (architecture), division of feature development tasks, and consistent updates to keep each other informed. 

## Project Design and Creativity

### Innovation and creativity

### User experience

## Conclusion
