from ..shell import run


def extract(filename, **kwargs):
    pipe = run(
        'tesseract %(filename)s tmpout && cat tmpout.txt && rm -f tmpout.txt'
        % locals())
    return pipe.stdout.read()
