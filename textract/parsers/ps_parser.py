from .utils import ShellParser  # noqa: D100


class Parser(ShellParser):
    """Extract text from postscript files using ps2ascii command."""

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102
        stdout, _ = self.run(["ps2ascii", filename])
        return stdout
