import sys

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from postscript files using ps2ascii command.
    On Windows, uses gswin64c directly since ps2ascii is Unix-only.
    """

    def extract(self, filename, **kwargs):
        if sys.platform == 'win32':
            stdout, _ = self.run([
                'gswin64c', '-q', '-dNODISPLAY', '-dBATCH', '-dNOPAUSE',
                '-sDEVICE=txtwrite', '-sOutputFile=-', filename,
            ])
            return stdout

        stdout, _ = self.run(['ps2ascii', filename])
        return stdout
