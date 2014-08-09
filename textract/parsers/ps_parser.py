from ..shell import run


def extract(filename, **kwargs):
    """Extract text from postscript files using pstotext command.
    """
    stdout, stderr = run('pstotext %(filename)s' % locals())
    return stdout
