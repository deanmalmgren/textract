from ..shell import run
from ..exceptions import UnknownMethod, ShellError


def extract(filename, method='', **kwargs):
    """Extract text from pdf files using ``method``.
    """
    if method == '' or method == 'pdftotext':
        try:
            return extract_pdftotext(filename)
        except ShellError, e:

            # if pdftotext isn't installed and the pdftotext method
            # wasn't specified, then gracefully fallback to using
            # pdfminer instead
            if method == '' and e.is_uninstalled():
                return extract_pdfminer(filename)
            else:
                raise e

    elif method == 'pdfminer':
        return extract_pdfminer(filename)
    else:
        raise UnknownMethod(method)


def extract_pdftotext(filename):
    """Extract text from pdfs using the pdftotext command line utility."""
    stdout, stderr = run('pdftotext %(filename)s -' % locals())
    return stdout


def extract_pdfminer(filename):
    """Extract text from pdfs using pdfminer."""
    stdout, stderr = run('pdf2txt.py %(filename)s' % locals())
    return stdout
