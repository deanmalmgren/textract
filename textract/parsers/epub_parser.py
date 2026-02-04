import zipfile
from bs4 import BeautifulSoup

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from epub"""

    def extract(self, filename, **kwargs):
        book = zipfile.ZipFile(filename)
        result = ''
        for text_name in self.__epub_sections(book):
            if not text_name.endswith("html"):
                continue
            soup = BeautifulSoup(book.open(text_name), features='lxml')
            html_content_tags = ['title', 'p', 'h1', 'h2', 'h3', 'h4']
            for child in soup.find_all(html_content_tags):
                inner_text = child.text.strip() if child.text else ""
                if inner_text:
                    result += inner_text + '\n'
        return result

    def __epub_sections(self, book):
        opf_paths = self.__get_opf_paths(book)
        return self.__get_item_paths(book, opf_paths)

    def __get_opf_paths(self, book):
        meta_inf = book.open("META-INF/container.xml")
        meta_soup = BeautifulSoup(meta_inf, features="xml")
        if not meta_soup.rootfiles:
            return []
        return [
            f.get("full-path")  # type: ignore[attr-defined]
            for f in meta_soup.rootfiles.find_all("rootfile")
            if f.get("full-path")  # type: ignore[attr-defined]
        ]

    def __get_item_paths(self, book, opf_paths):
        item_paths = []
        for opf_path in opf_paths:
            opf_soup = BeautifulSoup(book.open(opf_path), "xml")
            if not opf_soup.spine:
                continue
            epub_items = opf_soup.spine.find_all("itemref")
            for epub_item in epub_items:
                if idref := epub_item.get("idref"):  # type: ignore[attr-defined]
                    item = self.__get_item(opf_soup, idref)
                    if item and (href := item.get("href")):  # type: ignore[attr-defined]
                        item_paths.append(self.__get_full_item_path(book, href))
        return item_paths

    def __get_item(self, opf_soup, item_id):
        if not opf_soup.manifest:
            return None
        for item in opf_soup.manifest.find_all("item"):
            if item.get("id") == item_id:  # type: ignore[attr-defined]
                return item
        return None

    def __get_full_item_path(self, book, partial_path):
        for filename in book.namelist():
            if filename.endswith(partial_path):
                return filename
        return None
