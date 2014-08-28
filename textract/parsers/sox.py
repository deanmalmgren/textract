"""
Convert an audio file to-and-from various formats, using sox.
"""

from .utils import ShellParser


class Parser(ShellParser):
    """
    Convert file to .wav, for use with wav_parser
    Note: for testing, use -
    http://www.text2speech.org/,
    with American Male 2 for best results
    """

    def extract(self, filename, **kwargs):
        command = (
            'sox -G -c 1 "%(filename)s" {0}.wav && '
            'textract {0}.wav && '
            'rm -f {0}.wav'
        )
        temp_filename = self.temp_filename()
        stdout, _ = self.run(command.format(temp_filename) % locals())
        return stdout
