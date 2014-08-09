from ..shell import run


def extract(filename, **kwargs):
    """Extract text from doc files using antiword.
    """
    stdout, stderr = run('antiword %(filename)s' % locals())
    return stdout
