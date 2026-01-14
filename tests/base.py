import pathlib
import shutil
import subprocess  # noqa: S404
import tempfile

import six

import textract


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
        lines = [line for line in lines if line.strip()]  # Clean empty lines
        return six.b("\n").join(lines)


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
            "COMMAND FAILED: {command}".format(**locals())
        )

    def assertSuccessfulTextract(self, filename, cleanup=True, **kwargs):  # noqa: D102, FBT002, N802
        # construct the option string
        option = self.get_cli_options(**kwargs)

        # run the command and make sure everything worked correctly
        temp_filename = self.get_temp_filename()
        self.assertSuccessfulCommand(
            "textract {option} '{filename}' > {temp_filename}".format(**locals()),
        )
        if cleanup:
            pathlib.Path(temp_filename).unlink()
            return None
        return temp_filename

    def compare_cli_output(self, filename, expected_filename=None, **kwargs):  # noqa: D102
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        # run the command and make sure everything worked correctly
        temp_filename = self.assertSuccessfulTextract(filename, cleanup=False, **kwargs)
        assert temp_filename is not None

        self.assertSuccessfulCommand(
            "diff --ignore-blank-lines '{temp_filename}' '{expected_filename}'".format(
                **locals(),
            ),
        )
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
