import os
import subprocess
import tempfile
import shutil


class BaseParserTestCase(object):
    """This BaseParserTestCase object is used to collect a bunch of
    standardized tests that should be run for every BaseParser.
    """

    # 'txt', for example. this is mandatory and potentially the only thing that
    #  has to be specified to subclass this unittest
    extension = ''

    # User can specify a particular filename root (without
    # extension!), but these have good defaults that are specified by
    # the @property methods below
    raw_text_filename_root = ''
    standardized_text_filename_root = ''
    unicode_text_filename_root = ''

    def __init__(self, *args, **kwargs):
        super(BaseParserTestCase, self).__init__(*args, **kwargs)
        if self.extension == '':
            raise NotImplementedError(
                'need to specify `extension` class attribute on test case'
            )

    def get_filename(self, filename_root, default_filename_root):
        if filename_root:
            filename = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                self.extension,
                filename_root + '.' + self.extension,
            )
            if not os.path.exists(filename):
                raise Exception((
                    'expected filename "%(filename)s" to exist for testing '
                    'purposes but it doesnt'
                ) % locals())
            return filename
        return self.get_filename(default_filename_root, default_filename_root)
        
    @property
    def raw_text_filename(self):
        return self.get_filename(self.raw_text_filename_root,
                                 "raw_text")

    @property
    def standardized_text_filename(self):
        return self.get_filename(self.standardized_text_filename_root,
                                 "standardized_text")

    @property
    def unicode_text_filename(self):
        return self.get_filename(self.unicode_text_filename_root,
                                 "unicode_text")

    def test_raw_text(self):
        """This tests an arbitrarily specified raw text file that is
        contributed by the user
        """
        self.compare_cli_output(self.raw_text_filename)
        self.compare_python_output(self.raw_text_filename)

    # def test_standardized_text(self):
    #     """This tests a standardized text output that should be identical
    #     across all filetypes (e.g., #49)
    #     """
    #     self.compare_cli_output(self.standardized_text_filename)
    #     self.compare_python_output(self.standardized_text_filename)

    # def test_unicode_text(self):
    #     """This tests a unicode text output
    #     """
    #     self.compare_cli_output(self.unicode_text_filename)
    #     self.compare_python_output(self.unicode_text_filename)

    def get_expected_filename(self, filename):
        basename, extension = os.path.splitext(filename)
        return basename + '.txt'

    def get_temp_filename(self):
        stream = tempfile.NamedTemporaryFile(delete=False)
        stream.close()
        return stream.name

    def assertSuccessfulCommand(self, command):
        self.assertEqual(
            0, subprocess.call(command, shell=True),
            "COMMAND FAILED: %(command)s" % locals()
        )

    def compare_cli_output(self, filename):
        expected_filename = self.get_expected_filename(filename)
        temp_filename = self.get_temp_filename()
        self.assertSuccessfulCommand(
           "textract %(filename)s > %(temp_filename)s" % locals()
        )
        self.assertSuccessfulCommand(
            "diff %(temp_filename)s %(expected_filename)s" % locals()
        )
        os.remove(temp_filename)

    def compare_python_output(self, filename):
        import textract
        result = textract.process(filename)
        with open(self.get_expected_filename(filename)) as stream:
            self.assertEqual(result.strip(), stream.read().strip())


class ShellParserTestCase(BaseParserTestCase):
    """This BaseParserTestCase object is used to collect a bunch of
    standardized tests that should be run for every ShellParser.
    """

    def test_filename_spaces(self):
        spaced_filename = self.get_temp_filename()
        spaced_filename += " a filename with spaces." + self.extension
        shutil.copyfile(self.raw_text_filename, spaced_filename)
        temp_filename = self.get_temp_filename()
        expected_filename = self.get_expected_filename(self.raw_text_filename)
        self.assertSuccessfulCommand(
           "textract '%(spaced_filename)s' > %(temp_filename)s" % locals()
        )
        self.assertSuccessfulCommand(
           "diff %(temp_filename)s %(expected_filename)s" % locals()
        )
        os.remove(spaced_filename)
        os.remove(temp_filename)
