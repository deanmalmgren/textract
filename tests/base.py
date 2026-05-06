import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import textract


def _normalize_whitespace(content: bytes) -> list[bytes]:
    """Normalize whitespace for comparison.

    Converts all whitespace (tabs, spaces, nbsp, etc.) to single spaces,
    removes blank lines, and normalizes line endings.
    """
    # Split into lines and filter blanks
    lines = [line for line in content.splitlines() if line.strip()]
    # Normalize whitespace within each line:
    # - Replace tabs, CR, nbsp (\xc2\xa0), and multiple spaces with single space
    # - Strip leading/trailing whitespace from each line
    normalized = []
    for line in lines:
        # Replace whitespace variants, collapse spaces, and strip
        processed = (
            line.replace(b"\t", b" ")
            .replace(b"\r", b" ")
            .replace(b"\xc2\xa0", b" ")  # nbsp in UTF-8
        )
        processed = re.sub(rb" +", b" ", processed).strip()
        if processed:  # Keep non-empty lines
            normalized.append(processed)
    return normalized


def _files_equal_ignore_blank_lines(file1: str, file2: str) -> bool:
    """Compare two files, ignoring blank lines and normalizing whitespace."""
    content1 = Path(file1).read_bytes()
    content2 = Path(file2).read_bytes()
    lines1 = _normalize_whitespace(content1)
    lines2 = _normalize_whitespace(content2)
    return lines1 == lines2


def _format_diff_message(lines1: list[bytes], lines2: list[bytes], header: str) -> str:
    msg_parts = [f"\n{header}", f"Line counts: {len(lines1)} vs {len(lines2)}"]

    min_lines = min(len(lines1), len(lines2))
    first_diff_idx = next((i for i in range(min_lines) if lines1[i] != lines2[i]), None)

    if first_diff_idx is not None:
        msg_parts.extend(
            [
                f"First difference at line {first_diff_idx + 1}:",
                f"  Actual:   {lines1[first_diff_idx]!r}",
                f"  Expected: {lines2[first_diff_idx]!r}",
            ]
        )
    elif len(lines1) != len(lines2):
        msg_parts.append("Files differ in length (all common lines match)")

    msg_parts.append("\nActual output (first 3 lines):")
    msg_parts.extend(f"  {i + 1}: {line!r}" for i, line in enumerate(lines1[:3]))
    msg_parts.append("\nExpected output (first 3 lines):")
    msg_parts.extend(f"  {i + 1}: {line!r}" for i, line in enumerate(lines2[:3]))

    return "\n".join(msg_parts)


def _generate_file_diff_message(file1: str, file2: str) -> str:
    """Generate detailed diff message for file comparison failures."""
    content1 = Path(file1).read_bytes()
    content2 = Path(file2).read_bytes()
    return _format_diff_message(
        _normalize_whitespace(content1),
        _normalize_whitespace(content2),
        f"Files differ: {file1} vs {file2}",
    )


def _generate_bytes_diff_message(actual: bytes, expected: bytes, label: str) -> str:
    """Generate detailed diff message comparing actual bytes against expected bytes."""
    return _format_diff_message(
        _normalize_whitespace(actual),
        _normalize_whitespace(expected),
        f"Python output differs from {label}",
    )


class GenericUtilities:
    def get_temp_filename(self, extension=None):
        stream = tempfile.NamedTemporaryFile(delete=False)
        stream.close()
        filename = stream.name
        if extension is not None:
            filename += "." + extension
            shutil.move(stream.name, filename)
        return filename

    def clean_text(self, text):
        lines = text.splitlines()
        # Clean empty lines (fixes epub issue)
        cleaned_lines = []
        for line in lines:
            if not line.strip():
                continue
            # Normalize tabs and nbsp to spaces, but preserve multiple spaces for layout
            processed = (
                line.replace(b"\t", b" ")
                .replace(b"\r", b"")
                .replace(b"\xc2\xa0", b" ")  # nbsp in UTF-8
                .rstrip()  # Only strip trailing whitespace
            )
            if processed:
                cleaned_lines.append(processed)
        return b"\n".join(cleaned_lines)


class BaseParserTestCase(GenericUtilities):
    """Collect standardized tests for every BaseParser.

    This BaseParserTestCase object provides a set of standard tests
    that should be run for each file format parser.
    """

    # 'txt', for example. this is mandatory and potentially the only thing that
    #  has to be specified to subclass this unittest
    extension = ""

    # User can specify a particular filename root (without
    # extension!), but these have good defaults that are specified by
    # the @property methods below
    raw_text_filename_root = ""
    standardized_text_filename_root = ""
    unicode_text_filename_root = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.extension:
            raise NotImplementedError(
                "need to specify `extension` class attribute on test case",
            )

    def get_extension_directory(self):
        return str(Path(__file__).resolve().parent / self.extension)

    def get_filename(self, filename_root, default_filename_root):
        if filename_root:
            filename = str(
                Path(self.get_extension_directory())
                / f"{filename_root}.{self.extension}",
            )
            if not Path(filename).exists():
                msg = (
                    f'expected filename "{filename}" to exist for testing '
                    f"purposes but it doesn't"
                )
                raise FileNotFoundError(msg)
            return filename
        return self.get_filename(default_filename_root, default_filename_root)

    @property
    def raw_text_filename(self):
        return self.get_filename(self.raw_text_filename_root, "raw_text")

    @property
    def standardized_text_filename(self):
        return self.get_filename(
            self.standardized_text_filename_root,
            "standardized_text",
        )

    @property
    def unicode_text_filename(self):
        return self.get_filename(self.unicode_text_filename_root, "unicode_text")

    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line."""
        self.compare_cli_output(self.raw_text_filename)

    def test_raw_text_python(self):
        """Make sure raw text matches from python."""
        self.compare_python_output(self.raw_text_filename)

    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line."""
        temp_filename = self.assertSuccessfulTextract(
            self.standardized_text_filename,
            cleanup=False,
        )
        assert temp_filename is not None
        content = Path(temp_filename).read_bytes()
        expected = self.get_standardized_text()
        assert b"".join(content.split()) == expected
        Path(temp_filename).unlink()

    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        result = textract.process(self.standardized_text_filename)
        expected = self.get_standardized_text()
        assert b"".join(result.split()) == expected

    def get_expected_filename(self, filename, **kwargs):
        path = Path(filename)
        basename = path.stem
        if method := kwargs.get("method"):
            basename += f"-m={method}"
        return str(path.parent / f"{basename}.txt")

    def get_cli_options(self, **kwargs):
        option = ""
        for key, val in kwargs.items():
            option += f"--{key}={val} "
        return option

    def get_standardized_text(self):
        filename = Path(self.get_extension_directory()) / "standardized_text.txt"
        if filename.exists():
            standardized_text = filename.read_bytes()
        else:
            standardized_text = b"the quick brown fox jumps over the lazy dog"
        return b"".join(standardized_text.split())

    def assertSuccessfulCommand(self, command):
        assert subprocess.call(command, shell=True) == 0, f"COMMAND FAILED: {command}"

    def assertSuccessfulTextract(self, filename, cleanup=True, **kwargs):
        option = self.get_cli_options(**kwargs)
        temp_filename = self.get_temp_filename()

        # Build command arguments
        cmd = ["textract"]
        if option.strip():
            cmd.extend(option.strip().split())
        cmd.append(filename)

        # Run command and write output to file
        with Path(temp_filename).open("wb") as output_file:
            result = subprocess.run(
                cmd,
                stdout=output_file,
                stderr=subprocess.PIPE,
                check=False,
            )

        assert result.returncode == 0, (
            f"textract command failed with exit code {result.returncode}: "
            f"{result.stderr.decode('utf-8', errors='ignore')}"
        )

        if cleanup:
            Path(temp_filename).unlink()
            return None
        return temp_filename

    def compare_cli_output(self, filename, expected_filename=None, **kwargs):
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        temp_filename = self.assertSuccessfulTextract(filename, cleanup=False, **kwargs)
        assert temp_filename is not None
        if not _files_equal_ignore_blank_lines(temp_filename, expected_filename):
            diff_msg = _generate_file_diff_message(temp_filename, expected_filename)
            Path(temp_filename).unlink()
            raise AssertionError(diff_msg)
        Path(temp_filename).unlink()

    def compare_python_output(self, filename, expected_filename=None, **kwargs):
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        result = textract.process(filename, **kwargs)
        expected_content = Path(expected_filename).read_bytes()
        cleaned_result = self.clean_text(result)
        cleaned_expected = self.clean_text(expected_content)
        if cleaned_result != cleaned_expected:
            diff_msg = _generate_bytes_diff_message(
                cleaned_result, cleaned_expected, expected_filename
            )
            raise AssertionError(diff_msg)


class ShellParserTestCase(BaseParserTestCase):
    """Collect standardized tests for every ShellParser.

    This BaseParserTestCase object extends BaseParserTestCase with tests
    specific to parsers that use shell commands.
    """

    def test_filename_spaces(self):
        """Make sure filenames with spaces work on the command line."""
        temp_filename = spaced_filename = self.get_temp_filename()
        spaced_filename += " a filename with spaces." + self.extension
        shutil.copyfile(self.raw_text_filename, spaced_filename)
        try:
            self.compare_cli_output(
                spaced_filename,
                self.get_expected_filename(self.raw_text_filename),
            )
        finally:
            Path(temp_filename).unlink(missing_ok=True)
            Path(spaced_filename).unlink(missing_ok=True)
