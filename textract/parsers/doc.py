from ..shell import run


def extract(filename, **kwargs):
    """Extract text from doc files using antiword.
    """
    pipe = run('antiword %(filename)s' % locals())
    return pipe.stdout.read()
