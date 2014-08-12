from .utils import ShellParser


class Parser(ShellParser):

    def extract(self, filename, **kwargs):
        """Extract text from postscript files using pstotext command.
        """
        stdout, _ = self.run('pstotext %(filename)s' % locals())
        return stdout
