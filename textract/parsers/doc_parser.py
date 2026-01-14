from .utils import ShellParser  # noqa: D100


class Parser(ShellParser):
    """Extract text from doc files using antiword."""

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102
        stdout, _stderr = self.run(["antiword", filename])
        return stdout
