from ..shell import run


def extract(filename):
    """Extract text from doc files using antiword.
    """
    pipe = run('antiword %(filename)s' % locals())
    return pipe.stdout.read()
