from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

from .utils import BaseParser, _call_with_kwargs


class Parser(BaseParser):
    """Extract text from epub using python epub library
    """

    def extract(self, filename, **kwargs):
        book = _call_with_kwargs(epub.read_epub, filename, **kwargs)
        result = ''
        for id, _ in book.spine:
            item = book.get_item_with_id(id)
            soup = BeautifulSoup(item.content, 'lxml')
            for child in soup.find_all(
                ['title', 'p', 'div', 'h1', 'h2', 'h3', 'h4']
            ):
                result = result + child.text + '\n'
        return result
