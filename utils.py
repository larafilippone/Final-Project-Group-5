import webbrowser
from config import SEARCH_PARAMS

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

def value_to_key(search_value):
    """
    The function iterates through the SEARCH_PARAMS dictionary, compares each value with 
    the provided search_value, and returns the key corresponding to that value. If the 
    provided value is not found in the dictionary, the function returns None.

    Arguments:
    search_value (str): the value for which the corresponding key in the SEARCH_PARAMS 
                        dictionary needs to be found.

    Returns:
    str or None: the key corresponding to the provided search_value in the SEARCH_PARAMS 
                 dictionary. Returns None if the value is not found in the dictionary.
    """
    for key, value in SEARCH_PARAMS.items():
        if value == search_value:
            return key
    return None