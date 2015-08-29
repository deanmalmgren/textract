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

        # Tesseract can't output to console directly so you must first create
        # a dummy file to write to, read, and then delete
        devnull = os.devnull
        command = (
            'tesseract "%(filename)s" %(lang)s {0} > %(devnull)s && '
            'cat {0}.txt && '
            'rm -f {0} {0}.txt'
        )
        temp_filename = self.temp_filename()
        stdout, _ = self.run(command.format(temp_filename) % locals())
        return stdout
