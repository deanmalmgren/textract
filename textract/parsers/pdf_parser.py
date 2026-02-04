import os  # noqa: D100
import pathlib
import platform
import shutil
import sys
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
    """

    def extract(self, filename, method='', **kwargs):
        if method in {"", "pdftotext"}:
            try:
                return self.extract_pdftotext(filename, **kwargs)
            except ShellError as ex:
                # If pdftotext isn't installed and the pdftotext method
                # wasn't specified, then gracefully fallback to using
                # pdfminer instead.
                if method == '' and ex.is_not_installed():
                    return self.extract_pdfminer(filename, **kwargs)
                raise

        elif method == 'pdfminer':
            return self.extract_pdfminer(filename, **kwargs)
        elif method == 'tesseract':
            return self.extract_tesseract(filename, **kwargs)
        else:
            raise UnknownMethod(method)

    def extract_pdftotext(self, filename, **kwargs):
        """Extract text from pdfs using the pdftotext command line utility."""
        if 'layout' in kwargs:
            args = ['pdftotext', '-layout', filename, '-']
        else:
            args = ['pdftotext', filename, '-']
        stdout, _ = self.run(args)
        return stdout

    def extract_pdfminer(self, filename, **kwargs):
        """Extract text from pdfs using pdfminer."""
        # Find pdf2txt script
        pdf2txt_path = which("pdf2txt.py")

        # If not found via which, look in Scripts/bin directory
        if pdf2txt_path is None:
            bin_dir = pathlib.Path(sys.executable).parent
            potential_paths = [
                bin_dir / "pdf2txt.py",  # Unix: .venv/bin/pdf2txt.py
                bin_dir / "Scripts" / "pdf2txt.py",  # Windows: .venv/Scripts/pdf2txt.py
            ]
            for path in potential_paths:
                if path.exists():
                    pdf2txt_path = str(path)
                    break

        if pdf2txt_path is None:
            msg = "pdf2txt.py not found in environment"
            raise ShellError("pdf2txt.py", 127, "", msg)

        # On Windows, always use sys.executable; on Unix, try direct execution first
        if platform.system() == "Windows":
            stdout, _ = self.run([sys.executable, pdf2txt_path, filename])
        else:
            try:
                stdout, _ = self.run(["pdf2txt.py", filename])
            except (OSError, ShellError):
                # Fallback to using sys.executable
                stdout, _ = self.run([sys.executable, pdf2txt_path, filename])
        return stdout

    def extract_tesseract(self, filename, **kwargs):
        """Extract text from pdfs using tesseract (per-page OCR)."""
        temp_dir = mkdtemp()
        base = os.path.join(temp_dir, 'conv')
        contents = []
        try:
            stdout, _ = self.run(['pdftoppm', filename, base])

            for page in sorted(os.listdir(temp_dir)):
                page_path = os.path.join(temp_dir, page)
                page_content = TesseractParser().extract(page_path, **kwargs)
                contents.append(page_content)
            return six.b('').join(contents)
        finally:
            shutil.rmtree(temp_dir)
