import functools
import unittest
import warnings

from bs4 import XMLParsedAsHTMLWarning

from . import base


def _ignore_xml_as_html_warning(test_method):
    # epub content documents are XHTML, so BeautifulSoup's lxml HTML parser
    # correctly warns that an XML parser would be more reliable. We keep the
    # lenient HTML parser deliberately: it recovers from the malformed markup
    # found in real-world epubs better than the XML parser does.
    @functools.wraps(test_method)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
            return test_method(*args, **kwargs)

    return wrapper


class EpubTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "epub"

    @_ignore_xml_as_html_warning
    def test_raw_text_python(self):
        super().test_raw_text_python()

    @_ignore_xml_as_html_warning
    def test_standardized_text_python(self):
        super().test_standardized_text_python()
