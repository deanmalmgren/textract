from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from epub using python epub library
    """

    def extract(self, filename, **kwargs):
        book = epub.read_epub(filename)
        result = ""
        for item in book.get_items():
            type = item.get_type()
            if type == ITEM_DOCUMENT:
                soup = BeautifulSoup(item.content, 'lxml')
                result = result + soup.text
        return result
