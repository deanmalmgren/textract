from __future__ import annotations

import shutil
from pathlib import Path
from tempfile import mkdtemp

from textract.exceptions import LibreOfficeNotFound, ShellError

from .utils import ShellParser

_SOFFICE_CANDIDATES = (
    "soffice",
    "libreoffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/libreoffice/program/soffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
)


def _find_soffice() -> str | None:
    for candidate in _SOFFICE_CANDIDATES:
        if resolved := shutil.which(candidate):
            return resolved
        if Path(candidate).is_file():
            return candidate
    return None


class Parser(ShellParser):
    """Extract text from legacy .doc files using LibreOffice.

    LibreOffice is an optional runtime dependency: if the ``soffice``
    executable can't be found, a :class:`.LibreOfficeNotFound` error is
    raised explaining how to install it or pre-convert the file.
    """

    def extract(self, filename, **kwargs):
        soffice = _find_soffice()
        if soffice is None:
            raise LibreOfficeNotFound()

        temp_dir = mkdtemp()
        try:
            profile_uri = (Path(temp_dir) / "profile").as_uri()
            stdout, stderr = self.run(
                [
                    soffice,
                    "--headless",
                    f"-env:UserInstallation={profile_uri}",
                    "--convert-to",
                    "txt:Text (encoded):UTF8",
                    "--outdir",
                    temp_dir,
                    filename,
                ]
            )
            output = Path(temp_dir) / f"{Path(filename).stem}.txt"
            if not output.is_file():
                raise ShellError(
                    f"soffice --convert-to txt {filename}", 1, stdout, stderr
                )
            return output.read_text(encoding="utf-8-sig")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
