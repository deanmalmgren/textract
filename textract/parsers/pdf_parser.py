import os
import shutil
from tempfile import mkdtemp

from ..exceptions import UnknownMethod, ShellError

from .utils import ShellParser
from .image import Parser as TesseractParser


class Parser(ShellParser):
    """Extract text from pdf files using either the ``pdftotext`` method
    (default) or the ``pdfminer`` method.
    """

    def extract(self, filename, method='', **kwargs):
        if method == '' or method == 'pdftotext':
            try:
                return self.extract_pdftotext(filename, **kwargs)
            except ShellError as ex:
                # If pdftotext isn't installed and the pdftotext method
                # wasn't specified, then gracefully fallback to using
                # pdfminer instead.
                if method == '' and ex.is_not_installed():
                    return self.extract_pdfminer(filename, **kwargs)
                else:
                    raise ex

        elif method == 'pdfminer':
            return self.extract_pdfminer(filename, **kwargs)
        elif method == 'tesseract':
            return self.extract_tesseract(filename, **kwargs)
        else:
            raise UnknownMethod(method)

    def extract_pdftotext(self, filename, **kwargs):
        """Extract text from pdfs using the pdftotext command line utility."""
        if 'layout' in kwargs:
            layout = '-layout'
        else:
            layout = ''
        stdout, _ = self.run(
            'pdftotext %(layout)s "%(filename)s" -' % locals()
        )
        return stdout

    def extract_pdfminer(self, filename, **kwargs):
        """Extract text from pdfs using pdfminer."""
        stdout, _ = self.run('pdf2txt.py "%(filename)s"' % locals())
        return stdout

    def extract_tesseract(self, filename, **kwargs):
        """Extract text from pdfs using tesseract (per-page OCR)."""
        temp_dir = mkdtemp()
        base = os.path.join(temp_dir, 'conv')
        contents = []
        try:
            stdout, _ = self.run('pdftoppm "%s" "%s"' % (filename, base))

            for page in sorted(os.listdir(temp_dir)):
                page_path = os.path.join(temp_dir, page)
                page_content = TesseractParser().extract(page_path, **kwargs)
                contents.append(page_content)
            return ''.join(contents)
        finally:
            shutil.rmtree(temp_dir)
