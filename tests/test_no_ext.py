import unittest
import os
import textract

class No_Ext_TestCase(unittest.TestCase):

    def test_docx(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docx_file = os.path.join(current_dir, "tests/no_ext/docx_paragraphs_and_tables")
        # pass the file without extension and provide the extension as a parameter
        text = textract.process(docx_file, extension='docx')
        print(text)

    def test_msg(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        msg_file = os.path.join(current_dir, "tests/no_ext/msg_standardized_text")
        # pass the file without extension and provide the extension as a parameter
        text = textract.process(msg_file, extension='msg')
        print(text)

    def test_pdf(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_file = os.path.join(current_dir, "tests/no_ext/pdf_standardized_text")
        # pass the file without extension and provide the extension as a parameter
        text = textract.process(pdf_file, extension='.pdf')
        print(text)

