from ..shell import run


def extract(filename, **kwargs):
    """Tesseract cannot output to stdout directly so a tmp file must be
    created, read and then removed
    """
    pipe = run(
        'tesseract %(filename)s tmpout && cat tmpout.txt && rm -f tmpout.txt'
        % locals())
    return pipe.stdout.read()
