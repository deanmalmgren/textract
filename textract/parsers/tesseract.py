"""
Process an image file using tesseract.
"""

import tempfile
import os

from ..shell import run


def temp_filename():
    """
    Return a unique tempfile name.
    """
    handle, filename = tempfile.mkstemp()
    os.close(handle)
    return filename


def extract(filename, **kwargs):
    """Extract text from various image file formats using tesseract-ocr"""

    # Tesseract can't output to console directly so you must first
    # create a dummy file to write to, read, and then
    # delete. Depending on your Tesseract version, it also may print
    # tesseract version information to standard output
    devnull = os.devnull
    command = (
        'tesseract %(filename)s {0} > %(devnull)s && '
        'cat {0}.txt && '
        'rm -f {0} {0}.txt'
    )
    temp_name = temp_filename()
    stdout, _ = run(command.format(temp_name) % locals())
    return stdout
