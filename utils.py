import webbrowser

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

def open_amazon(product_url):
    webbrowser.open_new(product_url)