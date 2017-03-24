import textract
import os
import unittest


class NoExtTestCase(unittest.TestCase):

    def test(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        myfile = os.path.join(current_dir, "tests/docx/paragraphs_and_tables")
        # pass the file without extension and provide the extension as a parameter
        text = textract.process(myfile, extension='docx')
        print(text)


