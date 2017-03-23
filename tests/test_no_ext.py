import textract
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



myfile = os.path.join(current_dir, "tests/docx/paragraphs_and_tables.docx")
# pass the file with extension
text = textract.process(myfile)
print(text)

myfile = os.path.join(current_dir, "tests/docx/paragraphs_and_tables")
# pass the file without extension and provide the extension as a parameter
text = textract.process(myfile, extension='docx')
print(text)
