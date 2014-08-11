"""This module includes a bunch of convenient base classes that are
reused in many of the other parser modules.
"""

import subprocess

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
        """Encode the ``text`` in ``encoding`` byte-encoding.
        """
        return text.encode(encoding)

    def process(self, filename, encoding, **kwargs):
        """Process ``filename`` and encode byte-string with ``encoding``.
        """
        return self.encode(self.extract(filename, **kwargs), encoding)        


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
            raise exceptions.ShellError(command, pipe.returncode)

        return stdout, stderr
