import os
import pathlib
import unittest

import textract


class No_Ext_TestCase(unittest.TestCase):
    def test_docx(self):
        current_dir = pathlib.Path(pathlib.Path(pathlib.Path(__file__).resolve()).parent).parent
        docx_file = os.path.join(current_dir, "tests/no_ext/docx_paragraphs_and_tables")
        # pass the file without extension and provide the extension as a parameter
        textract.process(docx_file, extension="docx")

    def test_msg(self):
        current_dir = pathlib.Path(pathlib.Path(pathlib.Path(__file__).resolve()).parent).parent
        msg_file = os.path.join(current_dir, "tests/no_ext/msg_standardized_text")
        # pass the file without extension and provide the extension as a parameter
        textract.process(msg_file, extension="msg")

    def test_pdf(self):
        current_dir = pathlib.Path(pathlib.Path(pathlib.Path(__file__).resolve()).parent).parent
        pdf_file = os.path.join(current_dir, "tests/no_ext/pdf_standardized_text")
        # pass the file without extension and provide the extension as a parameter
        textract.process(pdf_file, extension=".pdf")
