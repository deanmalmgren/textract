"""Custom exceptions for textract."""

from __future__ import annotations

from pathlib import Path

# Command not found exit code
_NOT_INSTALLED_EXIT_CODE = 127


# traceback from exceptions that inherit from this class are suppressed
class CommandLineError(Exception):
    """The traceback of all CommandLineError's is suppressed when the
    errors occur on the command line to provide a useful command line
    interface.
    """

    def render(self, msg: str) -> str:
        return msg % vars(self)


class ExtensionNotSupported(CommandLineError):
    """This error is raised with unsupported extensions"""

    def __init__(self, ext: str) -> None:
        """Initialize with unsupported extension."""
        self.ext = ext

        from .parsers import _get_available_extensions

        available_extensions = [
            e for e in _get_available_extensions() if e.startswith(".")
        ]
        self.available_extensions_str = ", ".join(available_extensions)

    def __str__(self):
        return self.render(
            (
                "The filename extension %(ext)s is not yet supported by\n"
                "textract. Please suggest this filename extension here:\n\n"
                "    https://github.com/deanmalmgren/textract/issues\n\n"
                "Available extensions include: %(available_extensions_str)s\n"
            )
        )


class ExtensionRequired(CommandLineError):
    """Raised when bytes/stream input has no filename to detect the
    extension from and the caller didn't pass one explicitly.
    """

    def __str__(self):
        return self.render(
            "An extension is required to process bytes/stream input since "
            "there is no filename to detect it from. Pass one explicitly, "
            'e.g. process_bytes(data, extension="pdf") or\n'
            "`textract --extension pdf -`.\n"
        )


class MissingFileError(CommandLineError):
    """This error is raised when the file can not be located at the
    specified path.
    """

    def __init__(self, filename: str) -> None:
        """Initialize with missing file path."""
        self.filename = filename
        p = Path(filename)
        self.root = p.stem
        self.ext = p.suffix

    def __str__(self):
        return self.render(
            (
                'The file "%(filename)s" can not be found.\n'
                "Is this the right path/to/file/you/want/to/extract%(ext)s?"
            )
        )


class UnknownMethod(CommandLineError):
    """This error is raised when the specified --method on the command
    line is unknown.
    """

    def __init__(self, method: str) -> None:
        """Initialize with unknown method name."""
        self.method = method

    def __str__(self):
        return self.render(
            ('The method "%(method)s" can not be found for this filetype.')
        )


class LibreOfficeNotFound(CommandLineError):
    """Raised when a ``.doc`` file needs LibreOffice but it can't be found."""

    def __str__(self):
        return self.render(
            "Extracting text from legacy .doc files requires LibreOffice\n"
            "(the `soffice` executable), which could not be found on your\n"
            "system or PATH. Either install it:\n\n"
            "    http://textract.readthedocs.org/en/latest/installation.html\n\n"
            "or convert the file to .docx (or .pdf) first and pass that to\n"
            "textract instead. To batch-convert with LibreOffice:\n\n"
            "    soffice --headless --convert-to docx --outdir out/ *.doc\n"
        )


class ShellError(CommandLineError):
    """This error is raised when a shell.run returns a non-zero exit code
    (meaning the command failed).
    """

    def __init__(
        self,
        command: str,
        exit_code: int,
        stdout: bytes,
        stderr: bytes,
        ext: str | None = None,
    ) -> None:
        """Initialize with command execution details."""
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.executable = self.command.split()[0]
        self.ext = ext

    def is_not_installed(self) -> bool:
        """Check if the command failed because executable is not installed."""
        return self.exit_code == _NOT_INSTALLED_EXIT_CODE

    def not_installed_message(self) -> str:
        """Format error message when executable is not installed."""
        filetype_note = f" (needed to process {self.ext} files)" if self.ext else ""
        return (
            "The command `{command}` failed because the executable\n"
            "`{executable}` is not installed on your system{filetype_note}.\n"
            "Install it, then see textract's installation docs if you hit\n"
            "further issues:\n\n"
            "    http://textract.readthedocs.org/en/latest/installation.html\n"
        ).format(**vars(self), filetype_note=filetype_note)

    def failed_message(self) -> str:
        """Format error message when command execution failed."""
        return (
            "The command `%(command)s` failed with exit code %(exit_code)d\n"
            "------------- stdout -------------\n"
            "%(stdout)s"
            "------------- stderr -------------\n"
            "%(stderr)s"
        ) % vars(self)

    def __str__(self) -> str:
        if self.is_not_installed():
            return self.not_installed_message()
        return self.failed_message()


class InvalidInputEncoding(CommandLineError):
    """Raised when ``input_encoding`` is a valid codec name but can't
    decode the file's bytes (i.e. the wrong codec was specified).
    """

    def __init__(
        self,
        encoding: str,
        reason: str,
        ext: str | None = None,
    ) -> None:
        """Initialize with the attempted encoding and the decode failure reason."""
        self.encoding = encoding
        self.reason = reason
        self.ext = ext

    def __str__(self):
        filetype_note = f" {self.ext} " if self.ext else " "
        return self.render(
            (
                "The input encoding %(encoding)s could not decode this"
                + filetype_note
                + "file:\n\n"
                "    %(reason)s\n\n"
                "Double check that --input-encoding/input_encoding matches "
                "the file's actual encoding, or omit it to let textract "
                "auto-detect it.\n"
            )
        )


class MissingModuleError(CommandLineError):
    """This error is raised when a dependency module is not installed."""

    def __init__(self, import_error: ImportError, ext: str | None = None) -> None:
        """Initialize with the underlying ImportError."""
        self.missing_module = import_error.name
        self.ext = ext

    def __str__(self):
        filetype_note = f" to extract text from {self.ext} files" if self.ext else ""
        return self.render(
            (
                "Module %(missing_module)s is not installed on your system,\n"
                "but is required" + filetype_note + ". Note that the PyPI\n"
                "package name doesn't always match the module name above\n"
                "(e.g. the `PIL` module comes from the `Pillow` package), so\n"
                "check textract's installation docs for the right package\n"
                "and any non-Python dependencies it needs:\n\n"
                "    http://textract.readthedocs.org/en/latest/installation.html\n"
            )
        )
