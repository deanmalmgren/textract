import pathlib
import shutil
import subprocess  # noqa: S404
import sys
import tempfile

import six

import textract


def _quote_path(path: str) -> str:
    """Quote a path for shell commands in a cross-platform way."""
    if sys.platform == "win32":
        return f'"{path}"'
    return f"'{path}'"


def _normalize_whitespace(content: bytes) -> list[bytes]:
    """Normalize whitespace for comparison.

    Converts all whitespace (tabs, spaces, nbsp, etc.) to single spaces,
    removes blank lines, and normalizes line endings.
    """
    import re
    # Split into lines and filter blanks
    lines = [line for line in content.splitlines() if line.strip()]
    # Normalize whitespace within each line:
    # - Replace tabs, CR, nbsp (\xc2\xa0), and multiple spaces with single space
    # - Strip leading/trailing whitespace from each line
    normalized = []
    for line in lines:
        # Replace common whitespace variants with space
        line = line.replace(b"\t", b" ")
        line = line.replace(b"\r", b" ")
        line = line.replace(b"\xc2\xa0", b" ")  # nbsp in UTF-8
        # Collapse multiple spaces to single space
        line = re.sub(rb" +", b" ", line)
        # Strip leading/trailing whitespace
        line = line.strip()
        if line:  # Keep non-empty lines
            normalized.append(line)
    return normalized


def _files_equal_ignore_blank_lines(file1: str, file2: str) -> bool:
    """Compare two files, ignoring blank lines and normalizing whitespace."""
    content1 = pathlib.Path(file1).read_bytes()
    content2 = pathlib.Path(file2).read_bytes()
    lines1 = _normalize_whitespace(content1)
    lines2 = _normalize_whitespace(content2)
    return lines1 == lines2


def _generate_file_diff_message(file1: str, file2: str) -> str:
    """Generate detailed diff message for file comparison failures."""
    content1 = pathlib.Path(file1).read_bytes()
    content2 = pathlib.Path(file2).read_bytes()
    lines1 = _normalize_whitespace(content1)
    lines2 = _normalize_whitespace(content2)

    msg_parts = [f"\nFiles differ: {file1} vs {file2}"]

    # Show line counts
    msg_parts.append(f"Line counts: {len(lines1)} vs {len(lines2)}")

    # Show first differing line
    min_lines = min(len(lines1), len(lines2))
    first_diff_idx = None
    for i in range(min_lines):
        if lines1[i] != lines2[i]:
            first_diff_idx = i
            break

    if first_diff_idx is not None:
        msg_parts.append(f"First difference at line {first_diff_idx + 1}:")
        msg_parts.append(f"  Actual:   {lines1[first_diff_idx]!r}")
        msg_parts.append(f"  Expected: {lines2[first_diff_idx]!r}")
    elif len(lines1) != len(lines2):
        msg_parts.append("Files differ in length (all common lines match)")

    # Show preview of actual content (first 3 lines)
    msg_parts.append("\nActual output (first 3 lines):")
    for i, line in enumerate(lines1[:3]):
        msg_parts.append(f"  {i + 1}: {line!r}")

    # Show preview of expected content (first 3 lines)
    msg_parts.append("\nExpected output (first 3 lines):")
    for i, line in enumerate(lines2[:3]):
        msg_parts.append(f"  {i + 1}: {line!r}")

    return "\n".join(msg_parts)


class GenericUtilities:  # noqa: D101
    def get_temp_filename(self, extension=None):  # noqa: D102, PLR6301
        stream = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
        stream.close()
        filename = stream.name
        if extension is not None:
            filename += "." + extension
            shutil.move(stream.name, filename)
        return filename

    def clean_text(self, text):  # noqa: D102, PLR6301
        lines = text.splitlines()
        # Clean empty lines (fixes epub issue)
        cleaned_lines = []
        for line in lines:
            if not line.strip():
                continue
            # Normalize tabs and nbsp to spaces, but preserve multiple spaces for layout
            line = line.replace(b"\t", b" ")
            line = line.replace(b"\r", b"")
            line = line.replace(b"\xc2\xa0", b" ")  # nbsp in UTF-8
            line = line.rstrip()  # Only strip trailing whitespace
            if line:
                cleaned_lines.append(line)
        return six.b("\n").join(cleaned_lines)


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

    def __init__(self, *args, **kwargs) -> None:  # noqa: D107
        super().__init__(*args, **kwargs)
        if not self.extension:
            raise NotImplementedError(
                "need to specify `extension` class attribute on test case",
            )

    def get_extension_directory(self):  # noqa: D102
        return str(pathlib.Path(__file__).resolve().parent / self.extension)

    def get_filename(self, filename_root, default_filename_root):  # noqa: D102
        if filename_root:
            filename = str(
                pathlib.Path(self.get_extension_directory())
                / f"{filename_root}.{self.extension}",
            )
            if not pathlib.Path(filename).exists():
                msg = (
                    f'expected filename "{filename}" to exist for testing '
                    f"purposes but it doesn't"
                )
                raise FileNotFoundError(msg)
            return filename
        return self.get_filename(default_filename_root, default_filename_root)

    @property
    def raw_text_filename(self):  # noqa: D102
        return self.get_filename(self.raw_text_filename_root, "raw_text")

    @property
    def standardized_text_filename(self):  # noqa: D102
        return self.get_filename(
            self.standardized_text_filename_root,
            "standardized_text",
        )

    @property
    def unicode_text_filename(self):  # noqa: D102
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
        content = pathlib.Path(temp_filename).read_bytes()
        expected = self.get_standardized_text()
        assert six.b("").join(content.split()) == expected
        pathlib.Path(temp_filename).unlink()

    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        result = textract.process(self.standardized_text_filename)
        expected = self.get_standardized_text()
        assert six.b("").join(result.split()) == expected

    def get_expected_filename(self, filename, **kwargs):  # noqa: D102, PLR6301
        path = pathlib.Path(filename)
        basename = path.stem
        if method := kwargs.get("method"):
            basename += f"-m={method}"
        return str(path.parent / f"{basename}.txt")

    def get_cli_options(self, **kwargs):  # noqa: D102, PLR6301
        option = ""
        for key, val in six.iteritems(kwargs):
            option += f"--{key}={val} "
        return option

    def get_standardized_text(self):  # noqa: D102
        filename = (
            pathlib.Path(self.get_extension_directory()) / "standardized_text.txt"
        )
        if filename.exists():
            standardized_text = filename.read_bytes()
        else:
            standardized_text = six.b("the quick brown fox jumps over the lazy dog")
        return six.b("").join(standardized_text.split())

    def assertSuccessfulCommand(self, command):  # noqa: D102, N802, PLR6301
        assert subprocess.call(command, shell=True) == 0, (  # noqa: S602
            f"COMMAND FAILED: {command}"
        )

    def assertSuccessfulTextract(self, filename, cleanup=True, **kwargs):  # noqa: D102, FBT002, N802
        option = self.get_cli_options(**kwargs)
        temp_filename = self.get_temp_filename()

        # Build command arguments
        cmd = ["textract"]
        if option.strip():
            cmd.extend(option.strip().split())
        cmd.append(filename)

        # Run command and write output to file
        with pathlib.Path(temp_filename).open("wb") as output_file:
            result = subprocess.run(  # noqa: S603
                cmd,  # noqa: S607
                stdout=output_file,
                stderr=subprocess.PIPE,
                check=False,
            )

        assert result.returncode == 0, (
            f"textract command failed with exit code {result.returncode}: "
            f"{result.stderr.decode('utf-8', errors='ignore')}"
        )

        if cleanup:
            pathlib.Path(temp_filename).unlink()
            return None
        return temp_filename

    def compare_cli_output(self, filename, expected_filename=None, **kwargs):  # noqa: D102
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        temp_filename = self.assertSuccessfulTextract(filename, cleanup=False, **kwargs)
        assert temp_filename is not None
        if not _files_equal_ignore_blank_lines(temp_filename, expected_filename):
            diff_msg = _generate_file_diff_message(temp_filename, expected_filename)
            pathlib.Path(temp_filename).unlink()
            raise AssertionError(diff_msg)
        pathlib.Path(temp_filename).unlink()

    def compare_python_output(self, filename, expected_filename=None, **kwargs):  # noqa: D102
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        result = textract.process(filename, **kwargs)
        expected_content = pathlib.Path(expected_filename).read_bytes()
        result = self.clean_text(result)
        expected = self.clean_text(expected_content)
        assert result == expected


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
        self.compare_cli_output(
            spaced_filename,
            self.get_expected_filename(self.raw_text_filename),
        )
        pathlib.Path(temp_filename).unlink()
        pathlib.Path(spaced_filename).unlink()
