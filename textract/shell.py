import subprocess

from . import exceptions


def run(command):
    """Run the specified shell command using Fabric-like behavior."""

    # run a subprocess and put the stdout and stderr on the pipe object
    pipe = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    pipe.wait()

    # if pipe is busted, raise an error (unlike Fabric)
    if pipe.returncode != 0:
        raise exceptions.ShellError(command, pipe.returncode)

    return pipe
