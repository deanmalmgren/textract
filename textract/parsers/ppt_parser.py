from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from ppt files using catppt.
    """

    def extract(self, filename, **kwargs):
        stdout, stderr = self.run('ppthtml "%(filename)s"' % locals())
        return stdout
