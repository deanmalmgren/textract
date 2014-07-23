import os


# traceback from exceptions that inherit from this class are suppressed
class CommandLineError(Exception):
    """The traceback of all CommandLineError's is supressed when the
    errors occur on the command line to provide a useful command line
    interface.
    """
    def render(self, msg):
        return msg % vars(self)


class ExtensionNotSupported(CommandLineError):
    """This error is raised with unsupported extensions"""
    def __init__(self, ext):
        self.ext = ext

    def __str__(self):
        return self.render((
            'The filename extension %(ext)s is not yet supported by\n'
            'textract. Please suggest this filename extension here:\n'
            '    https://github.com/deanmalmgren/textract/issues'
        ))


class MissingFileError(CommandLineError):
    """This error is raised when the file can not be located at the
    specified path.
    """
    def __init__(self, filename):
        self.filename = filename
        self.root, self.ext = os.path.splitext(filename)

    def __str__(self):
        return self.render((
            'The file "%(filename)s" can not be found.\n'
            'Is this the right path/to/file/you/want/to/extract%(ext)s?'
        ))


class UnknownMethod(CommandLineError):
    """This error is raised when the specified --method on the command
    line is unknown.
    """
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return self.render((
            'The method "%(method)s" can not be found for this filetype.'
        ))


class ShellError(CommandLineError):
    """This error is raised when a shell.run returns a non-zero exit code
    (meaning the command failed).
    """
    def __init__(self, exit_code):
        self.exit_code = exit_code

    def __str__(self):
        return "Command failed with exit code %s" % self.exit_code
