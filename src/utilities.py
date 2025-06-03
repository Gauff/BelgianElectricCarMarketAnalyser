import re
from datetime import datetime


def extract_year(string):

    if string is None:
        return None

    # Regular expression pattern to match the year
    pattern = r"\b\d{4}\b"  # Matches a 4-digit number

    # Search for the year in the string
    match = re.search(pattern, string)

    if match:
        # Extract the matched year
        year = int(match.group())

        if 2000 < int(year) <= datetime.now().year:
            return year

    # If no year found, return None or raise an error, depending on your use case
    return None


def extract_int(data):

    if data is None:
        return None

    pattern = r"\b\d*\b"

    # Search for the year in the string
    match = re.search(pattern, data)

    if match:
        # Extract the matched year
        number = int(match.group())
        return number
    else:
        # If no number found, return None or raise an error, depending on your use case
        return None
