from ..exceptions import UnknownMethod, ShellError

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from pdf files using either the ``pdftotext`` method
    (default) or the ``pdfminer`` method.
    """

    def extract(self, filename, method='', **kwargs):
        if method == '' or method == 'pdftotext':
            try:
                return self.extract_pdftotext(filename)
            except ShellError as ex:
                # If pdftotext isn't installed and the pdftotext method
                # wasn't specified, then gracefully fallback to using
                # pdfminer instead.
                if method == '' and ex.is_uninstalled():
                    return self.extract_pdfminer(filename)
                else:
                    raise ex

        elif method == 'pdfminer':
            return self.extract_pdfminer(filename)
        else:
            raise UnknownMethod(method)

    def extract_pdftotext(self, filename):
        """Extract text from pdfs using the pdftotext command line utility."""
        stdout, _ = self.run('pdftotext "%(filename)s" -' % locals())
        return stdout

    def extract_pdfminer(self, filename):
        """Extract text from pdfs using pdfminer."""
        stdout, _ = self.run('pdf2txt.py "%(filename)s"' % locals())
        return stdout
