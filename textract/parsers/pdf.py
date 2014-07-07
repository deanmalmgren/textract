from ..shell import run
from ..exceptions import UnknownMethod


def extract(filename, method=None, **kwargs):
    """Extract text from pdf files using ``method``.
    """
    method = method or 'pdftotext'
    if method == 'pdftotext':
        return extract_pdftotext(filename)
    elif method == 'pdfminer':
        return extract_pdfminer(filename)
    else:
        raise UnknownMethod(method)


def extract_pdftotext(filename):
    """Extract text from pdfs using the pdftotext command line utility."""
    pipe = run('pdftotext %(filename)s -' % locals())
    return pipe.stdout.read()


def extract_pdfminer(filename):
    """Extract text from pdfs using pdfminer."""
    pipe = run('pdf2txt.py %(filename)s' % locals())
    return pipe.stdout.read()
