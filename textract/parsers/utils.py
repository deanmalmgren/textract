"""This module includes a bunch of convenient base classes that are
reused in many of the other parser modules.
"""

import subprocess
import tempfile
import os

import chardet

from .. import exceptions


class BaseParser(object):
    """The BaseParser abstracts out some common functionality that is used
    across all document formats. Specifically, it owns the
    responsibility of handling all unicode and byte-encoding problems.

    Inspiration from http://nedbatchelder.com/text/unipain.html
    """

    def extract(self, filename, **kwargs):
        raise NotImplementedError('must be overridden by child classes')

    def encode(self, text, encoding):
        """Encode the ``text`` in ``encoding`` byte-encoding. This ignores
        code points that can't be encoded in byte-strings.
        """
        return text.encode(encoding, 'ignore')

    def process(self, filename, encoding, **kwargs):
        """Process ``filename`` and encode byte-string with ``encoding``.
        """
        # make a "unicode sandwich" to handle dealing with unknown
        # input byte strings and converting them to a predictable
        # output encoding
        # http://nedbatchelder.com/text/unipain/unipain.html#35
        byte_string = self.extract(filename, **kwargs)
        unicode_string = self.decode(byte_string)
        return self.encode(unicode_string, encoding)

    def decode(self, text):
        """Decode text using the chardet package
        """
        # only decode byte strings into unicode if it hasn't already
        # been done by a subclass
        if isinstance(text, unicode):
            return text

        # empty text? nothing to decode
        if not text:
            return u''

        # use chardet to automatically detect the encoding text
        max_confidence, max_encoding = 0.0, None
        result = chardet.detect(text)
        return text.decode(result['encoding'])


class ShellParser(BaseParser):
    """The ShellParser extends the BaseParser to make it easy to run
    external programs from the command line with Fabric-like behavior.
    """

    def run(self, command):
        """Run ``command`` and return the subsequent ``stdout`` and ``stderr``.
        """

        # run a subprocess and put the stdout and stderr on the pipe object
        pipe = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise exceptions.ShellError(
                command, pipe.returncode, stdout, stderr,
            )

        return stdout, stderr

    def temp_filename(self):
        """Return a unique tempfile name.
        """
        handle, filename = tempfile.mkstemp()
        os.close(handle)
        return filename
