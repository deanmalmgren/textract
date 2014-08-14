import xlrd


def extract(filename, **kwargs):
    """Extract text from Excel files(.xls/xlsx).
    """

    workbook = xlrd.open_workbook(filename)
    sheets_name = workbook.sheet_names()
    output = "\n"
    for names in sheets_name:
        worksheet = workbook.sheet_by_name(names)
        num_rows = worksheet.nrows
        num_cells = worksheet.ncols

        for curr_row in range(num_rows):
            row = worksheet.row(curr_row)
            new_output = [
                worksheet.cell_value(curr_row, index_col)
                for index_col in range(num_cells)
                if worksheet.cell_value(curr_row, index_col)
            ]
            if new_output:
                output += ' '.join(new_output) + '\n'
    return output
