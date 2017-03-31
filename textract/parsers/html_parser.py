import re
import six

from bs4 import BeautifulSoup

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from html file using beautifulsoup4. Filter text to
    only show the visible parts of the page. Insipration from `here
    <http://stackoverflow.com/a/1983219/564709>`_.
    """

    _disallowed_names = [
        'style', 'script', '[document]', 'head', 'title', 'html', 'meta',
        'link', 'body',
    ]

    _inline_tags = [
        'b', 'big', 'i', 'small', 'tt', 'abbr', 'acronym', 'cite', 'code',
        'dfn', 'em', 'kbd', 'strong', 'samp', 'var', 'a', 'bdo', 'br', 'img',
        'map', 'object', 'q', 'script', 'span', 'sub', 'sup', 'button',
        'input', 'label', 'select', 'textarea',
    ]

    def _visible(self, element):
        """Used to filter text elements that have invisible text on the page.
        """
        if element.name in self._disallowed_names:
            return False
        elif re.match(u'<!--.*-->', six.text_type(element.extract())):
            return False
        return True

    def _inline(self, element):
        """Used to check whether given element can be treated as inline
        element (without new line after).
        """
        if element.name in self._inline_tags:
            return True
        return False

    def _find_any_text(self, tag):
        """Looks for any possible text within given tag.
        """
        text = ''
        if tag is not None:
            text = six.text_type(tag)
            text = re.sub(r'(<[^>]+>)', '', text)
            text = re.sub(r'\s', ' ', text)
            text = text.strip()
        return text

    def _parse_tables(self, soup):
        """Returns array containing basic informations about tables for ASCII
        replacement (look: _replace_tables()).
        """
        tables = []
        for t in soup.find_all('table'):
            t_dict = {'width': 0, 'table': t, 'trs': [], 'col_width': {}}
            trs = t.find_all('tr')
            if len(trs) > 0:
                for tr in trs:
                    tr_dict = []
                    tds = tr.find_all('th') + tr.find_all('td')
                    if len(tds) > 0:
                        for i, td in enumerate(tds):
                            td_text = self._find_any_text(td)
                            length = len(td_text)
                            if i in t_dict['col_width']:
                                t_dict['col_width'][i] = max(
                                    length,
                                    t_dict['col_width'][i]
                                )
                            else:
                                t_dict['col_width'][i] = length
                            tr_dict.append({
                                'text': td_text,
                                'colspan': int(td.get('colspan', 1)),
                            })
                        t_dict['trs'].append(tr_dict)
                for col in t_dict['col_width']:
                    t_dict['width'] += t_dict['col_width'][col]
                tables.append(t_dict)
        return tables

    def _replace_tables(self, soup, v_separator=' | ', h_separator='-'):
        """Replaces <table> elements with its ASCII equivalent.
        """
        tables = self._parse_tables(soup)
        v_sep_len = len(v_separator)
        v_left_sep = v_separator.lstrip()
        for t in tables:
            html = ''
            trs = t['trs']
            h_length = 1 + (v_sep_len * len(t['col_width'])) + t['width']
            head_foot = (h_separator * h_length) + "\n"
            html += head_foot
            for tr in trs:
                html += v_left_sep
                for i, td in enumerate(tr):
                    text = td['text']
                    col_width = t['col_width'][i] + v_sep_len
                    if td['colspan'] > 1:
                        for j in range(td['colspan']-1):
                            j = j + 1
                            if (i+j) < len(t['col_width']):
                                col_width += t['col_width'][i+j] + v_sep_len
                    html += ('%' + str(col_width) + 's') % (text + v_separator)
                html += "\n"
            html += head_foot
            new_table = soup.new_tag('div')
            new_table.string = html
            t['table'].replace_with(new_table)
        return soup

    def _join_inlines(self, soup):
        """Unwraps inline elements defined in self._inline_tags.
        """
        elements = soup.find_all(True)
        for elem in elements:
            if self._inline(elem):
                elem.unwrap()
        return soup

    def extract(self, filename, **kwargs):
        with open(filename, "rb") as stream:
            soup = BeautifulSoup(stream, 'lxml')

        # Convert tables to ASCII ones
        soup = self._replace_tables(soup)

        # Join inline elements
        soup = self._join_inlines(soup)

        # Make HTML
        html = ''
        elements = soup.find_all(True)
        elements = [el for el in filter(self._visible, elements)]
        for elem in elements:
            string = elem.string
            if string is None:
                string = self._find_any_text(elem)
            string = string.strip()
            if len(string) > 0:
                html += "\n" + string + "\n"
        return html
