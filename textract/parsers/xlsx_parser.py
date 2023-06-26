import openpyxl as xl
import six
import datetime

from six.moves import xrange

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from Excel files (.xls/xlsx).
    """

    def extract(self, filename, **kwargs):
        workbook = xl.load_workbook(filename, data_only=True)
        sheets_name = workbook.sheetnames
        output = "\n"
        for names in sheets_name:
            worksheet = workbook[names]
            num_rows = worksheet.max_row
            num_cells = worksheet.max_column

            for curr_row, row in enumerate(worksheet.rows):
                new_output = []
                for index_col in xrange(num_cells):
                    value = worksheet.cell(curr_row+1, index_col+1)
                    value = value.value
                    if value:
                        if isinstance(value, (int, float)):
                            value = six.text_type(value)
                        if isinstance(value, datetime.datetime):
                            value = value.strftime("%m/%d/%Y, %H:%M:%S")
                        new_output.append(value)
                if new_output:
                    output += u' '.join(new_output) + u'\n'
        return output
