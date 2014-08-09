from ..shell import run


def extract(filename, **kwargs):
    """Extract text from various image file formats using tesseract-ocr"""
    # Tesseract can't output to console directly so you must first create
    # a dummy file to write to, read, and then delete
    stdout, stderr = run(
        'tesseract %(filename)s tmpout && cat tmpout.txt && rm -f tmpout.txt'
        % locals()
    )
    return stdout
