"""
Convert an audio file to-and-from various formats, using sox.
"""

from .utils import ShellParser


class Parser(ShellParser):
    """
    Convert file to .wav, for use with wav_parser
    """

    def extract(self, filename, **kwargs):
        command = (
            'sox "{0}" {1}.wav channels 1 && '
            'textract {1}.wav && '
            'rm -f {1}.wav'
        )
        temp_filename = self.temp_filename()
        stdout, _ = self.run(command.format(filename, temp_filename))
        return stdout
