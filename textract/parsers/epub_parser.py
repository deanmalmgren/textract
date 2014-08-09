from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


def extract(filename, **kwargs):
    """Extract text from epub using python epub library
    """
    book = epub.read_epub(filename)
    result = ""
    for item in book.get_items():
        type = item.get_type()
        if type == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content)
            result = result + soup.text
    return result
