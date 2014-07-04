# traceback from exceptions that inherit from this class are suppressed
class CommandLineError(Exception):
    pass


class ExtensionNotSupported(CommandLineError):
    def __init__(self, ext):
        self.ext = ext
    def __str__(self):
        return (
            'The filename extension %(ext)s is not yet supported by textract.\n'
            'Please suggest this filename extension here:\n'
            '    https://github.com/deanmalmgren/textract/issues'
        ) % vars(self)
