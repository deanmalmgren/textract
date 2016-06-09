"""
Process an image file using tesseract.
"""
import os

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from various image file formats using tesseract-ocr"""

    def extract(self, filename, **kwargs):

        # if language given as argument, specify language for tesseract to use
        if 'language' in kwargs:
            lang = '-l %s' % kwargs['language']
        else:
            lang = ''

        stdout, _ = self.run(['tesseract',filename,'stdout',lang])
        return stdout
