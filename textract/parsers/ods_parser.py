from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from OpenDocument Spreadsheet (.ods) files."""

    def extract(self, filename, **kwargs):
        document = load(filename)
        output = "\n"
        for table in document.getElementsByType(Table):
            for row in table.getElementsByType(TableRow):
                non_empty_values = [
                    value
                    for cell in row.getElementsByType(TableCell)
                    if (value := self.__cell_text(cell))
                ]
                if non_empty_values:
                    output += " ".join(non_empty_values) + "\n"
        return output

    def __cell_text(self, cell):
        value_type = cell.getAttribute("valuetype")
        if value_type == "boolean":
            return "1" if cell.getAttribute("booleanvalue") == "true" else None
        if value_type in ("float", "percentage", "currency"):
            return str(float(cell.getAttribute("value")))
        return "".join(str(p) for p in cell.getElementsByType(P)) or None
