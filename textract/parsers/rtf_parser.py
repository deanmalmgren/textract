import six  # noqa: D100

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from rtf files using unrtf."""

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102
        # http://superuser.com/a/243089/126633
        stdout, _stderr = self.run(["unrtf", "--text", filename])
        splitter = six.b("-") * 17 + six.b("\n")
        return stdout.split(splitter, 1)[-1]
