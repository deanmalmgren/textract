from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from doc files using antiword.
    """

    def extract(self, filename, **kwargs):
        stdout, stderr = self.run('antiword "%(filename)s"' % locals())
        return stdout
