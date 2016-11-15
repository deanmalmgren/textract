from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from postscript files using pstotext command.
    """

    def extract(self, filename, **kwargs):
        stdout, _ = self.run(['pstotext', filename])
        return stdout
