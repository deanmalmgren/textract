import openpyxl

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from Excel files (.xls/xlsx).
    """

    def extract(self, filename, **kwargs):
        workbook = openpyxl.load_workbook(filename=filename, read_only=True, data_only=True)
        sheets_name = workbook.sheetnames
        output = "\n"

        for names in sheets_name:
            worksheet = workbook[names]

            for row in worksheet.iter_rows():
                new_output = []
                for cell in row:
                    value = cell.value
                    if value:
                        if isinstance(value, (int, float)):
                            value = str(value)
                        new_output.append(value)
                if new_output:
                    output += u' '.join(new_output) + u'\n'
        return output
