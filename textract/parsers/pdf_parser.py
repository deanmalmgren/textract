import os  # noqa: D100
import shutil
from tempfile import mkdtemp

import six

from textract.exceptions import ShellError, UnknownMethod

from .image import Parser as TesseractParser
from .utils import ShellParser

try:
    from shutil import which
except ImportError:
    from distutils.spawn import find_executable as which


class Parser(ShellParser):
    """Extract text from pdf files using either the ``pdftotext`` method
    (default) or the ``pdfminer`` method.
    """  # noqa: D205

    def extract(self, filename, method="", **kwargs):  # noqa: ANN001, ANN201, D102
        if method in {"", "pdftotext"}:
            try:
                return self.extract_pdftotext(filename, **kwargs)
            except ShellError as ex:
                # If pdftotext isn't installed and the pdftotext method
                # wasn't specified, then gracefully fallback to using
                # pdfminer instead.
                if method == "" and ex.is_not_installed():  # noqa: PLC1901
                    return self.extract_pdfminer(filename, **kwargs)
                raise

        elif method == "pdfminer":
            return self.extract_pdfminer(filename, **kwargs)
        elif method == "tesseract":
            return self.extract_tesseract(filename, **kwargs)
        else:
            raise UnknownMethod(method)

    def extract_pdftotext(self, filename, **kwargs):  # noqa: ANN001, ANN201
        """Extract text from pdfs using the pdftotext command line utility."""
        if "layout" in kwargs:
            args = ["pdftotext", "-layout", filename, "-"]
        else:
            args = ["pdftotext", filename, "-"]
        stdout, _ = self.run(args)
        return stdout

    def extract_pdfminer(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002
        """Extract text from pdfs using pdfminer."""
        # Nested try/except loops? Not great
        # Try the normal pdf2txt, if that fails try the python3
        # pdf2txt, if that fails try the python2 pdf2txt
        pdf2txt_path = which("pdf2txt.py")
        try:
            stdout, _ = self.run(["pdf2txt.py", filename])
        except (OSError, ShellError):
            if pdf2txt_path is None:
                raise
            try:
                stdout, _ = self.run(["python3", pdf2txt_path, filename])
            except ShellError:
                stdout, _ = self.run(["python2", pdf2txt_path, filename])
        return stdout

    def extract_tesseract(self, filename, **kwargs):  # noqa: ANN001, ANN201
        """Extract text from pdfs using tesseract (per-page OCR)."""
        temp_dir = mkdtemp()
        base = os.path.join(temp_dir, "conv")  # noqa: PTH118
        contents = []
        try:
            _stdout, _ = self.run(["pdftoppm", filename, base])

            for page in sorted(os.listdir(temp_dir)):  # noqa: PTH208
                page_path = os.path.join(temp_dir, page)  # noqa: PTH118
                page_content = TesseractParser().extract(page_path, **kwargs)
                contents.append(page_content)
            return six.b("").join(contents)
        finally:
            shutil.rmtree(temp_dir)
