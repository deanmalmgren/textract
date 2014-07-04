import os


# traceback from exceptions that inherit from this class are suppressed
class CommandLineError(Exception):
    def render(self, msg):
        return msg % vars(self)


class ExtensionNotSupported(CommandLineError):
    def __init__(self, ext):
        self.ext = ext

    def __str__(self):
        return self.render((
            'The filename extension %(ext)s is not yet supported by\n'
            'textract. Please suggest this filename extension here:\n'
            '    https://github.com/deanmalmgren/textract/issues'
        ))


class MissingFileError(CommandLineError):
    def __init__(self, filename):
        self.filename = filename
        self.root, self.ext = os.path.splitext(filename)

    def __str__(self):
        return self.render((
            'The file "%(filename)s" can not be found.\n'
            'Is this the right path/to/file/you/want/to/extract%(ext)s?'
        ))
