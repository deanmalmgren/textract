import re

from bs4 import BeautifulSoup

disallowed_parents = set([
    'style',
    'script',
    '[document]',
    'head',
    'title',
])


def _visible(element):
    """Used to filter text elements that have invisible text on the page."""
    if element.parent.name in disallowed_parents:
        return False
    elif re.match(u'<!--.*-->', element):
        return False
    return True


def extract(filename, **kwargs):
    """Extract text from html file using beautifulsoup4. Filter text to
    only show the visible parts of the page. Insipration from `here
    <http://stackoverflow.com/a/1983219/564709>`_.
    """
    with open(filename) as stream:
        soup = BeautifulSoup(stream)

    # soup.get_text method is nice, but it also returns all the
    # embedded javascript which isn't terribly useful for this use
    # case. inspiration from http://stackoverflow.com/a/1983219/564709
    texts = soup.find_all(text=True)
    texts = [text.encode('utf-8') for text in filter(_visible, texts)]
    return '\n\n'.join(texts)
