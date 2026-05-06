import sys
from pathlib import Path

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from postscript files using ps2ascii command.
    On Windows, uses gswin64c directly since ps2ascii is Unix-only.
    """

    def extract(self, filename, **kwargs):
        if sys.platform == "win32":
            tmp = Path(self.temp_filename())
            try:
                self.run(
                    [
                        "gswin64c",
                        "-q",
                        "-dNODISPLAY",
                        "-dBATCH",
                        "-dNOPAUSE",
                        "-sDEVICE=txtwrite",
                        f"-sOutputFile={tmp}",
                        filename,
                    ]
                )
                return tmp.read_bytes()
            finally:
                tmp.unlink(missing_ok=True)

        stdout, _ = self.run(["ps2ascii", filename])
        return stdout
