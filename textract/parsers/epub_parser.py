# from ebooklib import epub, ITEM_DOCUMENT
from epubfile import Epub

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from epub using python epub library
    """

    def extract(self, filename, **kwargs):
        book = Epub(filename, read_only=True)
        result = ''
        for text_name in book.get_texts():
            soup = book.read_file(text_name, soup=True)
            # Don't fail with some AttributeError exception when the item is of NoneType
            # (i.e. at the last position).
            if soup is None:
                continue
            html_content_tags = ['title', 'p', 'h1', 'h2', 'h3', 'h4']
            for child in soup.find_all(html_content_tags):
                inner_text = child.text.strip() if child.text else ""
                if inner_text:
                    result += inner_text + '\n'
        return result
