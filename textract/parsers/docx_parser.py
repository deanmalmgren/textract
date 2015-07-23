import docx

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from docx file using python-docx.
    """

    def extract(self, filename, **kwargs):
        text = ""
        document = docx.Document(filename)

        # Extract text from root paragraphs.
        text += '\n\n'.join([
            paragraph.text for paragraph in document.paragraphs
        ])

        # Recursively extract text from root tables.
        for table in document.tables:
            text += self._parse_table(table, text)

        return text

    def _parse_table(self, table, text):
        for row in table.rows:
            for cell in row.cells:
                # For every cell in every row of the table, extract text from 
                # child paragraphs.
                text += '\n\n'.join([
                    paragraph.text for paragraph in cell
                ])

                # Then recursively extract text from child tables.
                for table in cell.tables:
                    text += _parse_table(table, text)

        return text
