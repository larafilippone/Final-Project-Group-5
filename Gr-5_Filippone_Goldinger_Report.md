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

### Code Overview
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

### Code Functionality and Quality

### Testing and Bug-Fixing

## Collaboration and Teamwork

### Team Roles and Responsibilities

### Collaboration Techniques

### Conflict Resolution

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
