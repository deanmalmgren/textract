from ..shell import run


def extract(filename, **kwargs):
    """Extract text from postscript files using pstotext command.
    """
    pipe = run('pstotext %(filename)s' % locals())
    return pipe.stdout.read()
