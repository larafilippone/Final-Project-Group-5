# Extracting Sentiment and Insights from Amazon Reviews to Improve Products

### Introduction to Computer Science and Programming

Lara Filippone, Florian Goldinger 25.01.2024

## Introduction

## Code Quality and Functionality

### Code overview

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

### Team roles and responsibilities

### Collaboration techniques

### Conflict resolution

## Project Design and Creativity

### Innovation and creativity

### User experience

## Conclusion
