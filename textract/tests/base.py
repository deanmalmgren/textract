import os
import subprocess
import tempfile
import shutil

import requests


class GenericUtilities(object):

    def get_temp_filename(self, extension=None):
        stream = tempfile.NamedTemporaryFile(delete=False)
        stream.close()
        filename = stream.name
        if not extension is None:
            filename += '.' + extension
            shutil.move(stream.name, filename)
        return filename


class BaseParserTestCase(GenericUtilities):
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

    def get_extension_directory(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.extension,
        )

    def get_filename(self, filename_root, default_filename_root):
        if filename_root:
            filename = os.path.join(
                self.get_extension_directory(),
                filename_root + '.' + self.extension,
            )
            if not os.path.exists(filename):
                raise Exception((
                    'expected filename "%(filename)s" to exist for testing '
                    'purposes but it doesnt'
                ) % locals())
            return filename
        return self.get_filename(default_filename_root, default_filename_root)

    def download_file(self, url, filename):
        if not os.path.exists(filename):

            # stream the request to make sure it works correctly
            # http://stackoverflow.com/a/16696317/564709
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as stream:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        stream.write(chunk)
                        stream.flush()

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

    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line"""
        self.compare_cli_output(self.raw_text_filename)

    def test_raw_text_python(self):
        """Make sure raw text matches from python"""
        self.compare_python_output(self.raw_text_filename)

    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line"""
        temp_filename = self.assertSuccessfulTextract(
            self.standardized_text_filename,
            cleanup=False,
        )
        with open(temp_filename) as stream:
            self.assertEqual(
                ''.join(stream.read().split()),
                self.get_standardized_text(),
                "standardized text fails for %s" % self.extension,
            )
        os.remove(temp_filename)

    def test_standardized_text_python(self):
        """Make sure standardized text matches from python"""
        import textract
        result = textract.process(self.standardized_text_filename)
        self.assertEqual(
            ''.join(result.split()),
            self.get_standardized_text(),
            "standardized text fails for %s" % self.extension,
        )

    # def test_unicode_text_cli(self):
    #     """Make sure unicode text matches from the command line"""
    #     self.compare_cli_output(self.unicode_text_filename)

    # def test_unicode_text_python(self):
    #     """Make sure unicode text matches from python"""
    #     self.compare_python_output(self.unicode_text_filename)

    def get_expected_filename(self, filename, **kwargs):
        basename, extension = os.path.splitext(filename)
        if kwargs.get('method'):
            basename += '-m=' + kwargs.get('method')
        return basename + '.txt'

    def get_cli_options(self, **kwargs):
        option = ''
        for key, val in kwargs.iteritems():
            option += '--%s=%s ' % (key, val)
        return option

    def get_standardized_text(self):
        filename = os.path.join(
            self.get_extension_directory(),
            "standardized_text.txt" + '.' + self.extension,
        )
        if os.path.exists(filename):
            with open(filename) as stream:
                standardized_text = stream.read()
        else:
            standardized_text = "the quick brown fox jumps over the lazy dog"
        return standardized_text.replace(' ','')

    def assertSuccessfulCommand(self, command):
        self.assertEqual(
            0, subprocess.call(command, shell=True),
            "COMMAND FAILED: %(command)s" % locals()
        )

    def assertSuccessfulTextract(self, filename, cleanup=True, **kwargs):

        # construct the option string
        option = self.get_cli_options(**kwargs)

        # run the command and make sure everything worked correctly
        temp_filename = self.get_temp_filename()
        self.assertSuccessfulCommand(
            "textract %(option)s '%(filename)s' > %(temp_filename)s" % locals()
        )
        if cleanup:
            os.remove(temp_filename)
            return None
        else:
            return temp_filename

    def compare_cli_output(self, filename, expected_filename=None, **kwargs):
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        # run the command and make sure everything worked correctly
        temp_filename = self.assertSuccessfulTextract(
            filename,
            cleanup=False,
            **kwargs
        )
        self.assertSuccessfulCommand(
            "diff '%(temp_filename)s' '%(expected_filename)s'" % locals()
        )
        os.remove(temp_filename)

    def compare_python_output(self, filename, expected_filename=None, **kwargs):
        if expected_filename is None:
            expected_filename = self.get_expected_filename(filename, **kwargs)

        import textract
        result = textract.process(filename, **kwargs)
        with open(expected_filename) as stream:
            self.assertEqual(result, stream.read())


class ShellParserTestCase(BaseParserTestCase):
    """This BaseParserTestCase object is used to collect a bunch of
    standardized tests that should be run for every ShellParser.
    """

    def test_filename_spaces(self):
        """Make sure filenames with spaces work on the command line"""
        temp_filename = spaced_filename = self.get_temp_filename()
        spaced_filename += " a filename with spaces." + self.extension
        shutil.copyfile(self.raw_text_filename, spaced_filename)
        self.compare_cli_output(
            spaced_filename,
            self.get_expected_filename(self.raw_text_filename),
        )
        os.remove(temp_filename)
        os.remove(spaced_filename)
