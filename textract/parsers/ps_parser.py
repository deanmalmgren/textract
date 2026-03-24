import os
import sys

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from postscript files using ps2ascii command.
    On Windows, uses gswin64c directly since ps2ascii is Unix-only.
    """

    def extract(self, filename, **kwargs):
        if sys.platform == 'win32':
            tmp = self.temp_filename()
            try:
                self.run([
                    'gswin64c', '-q', '-dNODISPLAY', '-dBATCH', '-dNOPAUSE',
                    '-sDEVICE=txtwrite', f'-sOutputFile={tmp}', filename,
                ])
                with open(tmp, 'rb') as f:
                    return f.read()
            finally:
                os.unlink(tmp)
        else:
            stdout, _ = self.run(['ps2ascii', filename])
            return stdout
