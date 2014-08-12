"""
Process an image file using tesseract.
"""

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from various image file formats using tesseract-ocr"""

    def extract(self, filename, **kwargs):

        # Tesseract can't output to console directly so you must first create
        # a dummy file to write to, read, and then delete
        cmd = 'tesseract %(filename)s {0} && cat {0}.txt && rm -f {0} {0}.txt'
        temp_filename = self.temp_filename()
        stdout, _ = self.run(cmd.format(temp_filename) % locals())
        return stdout
