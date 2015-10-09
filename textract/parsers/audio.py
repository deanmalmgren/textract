import speech_recognition as sr
import os

from .utils import ShellParser


class Parser(ShellParser):
    """
    Extract text (i.e. speech) from an audio file, using SpeechRecognition.

    Since SpeechRecognition expects a .wav file, with 1 channel,
    the audio file has to be converted, via sox, if not compliant

    Note: for testing, use -
    http://www2.research.att.com/~ttsweb/tts/demo.php,
    with Rich (US English) for best results
    """

    def extract(self, filename, **kwargs):
        speech = ''

        # convert to wav, if not already .wav
        base, ext = os.path.splitext(filename)
        if ext != '.wav':
            temp_filename = self.convert_to_wav(filename)
            try:
                speech = self.extract(temp_filename, **kwargs)
            finally:  # make sure temp_file is deleted
                os.remove(temp_filename)
        else:
            r = sr.Recognizer()

            with sr.WavFile(filename) as source:
                audio = r.record(source)

            try:
                speech = r.recognize_google(audio)
            except LookupError:  # audio is not understandable
                speech = ''

            # add a newline, to make output cleaner
            speech += '\n'

        return speech

    def convert_to_wav(self, filename):
        """
        Uses sox cmdline tool, to convert audio file to .wav

        Note: for testing, use -
        http://www.text2speech.org/,
        with American Male 2 for best results
        """
        command = (
            'sox -G -c 1 "%(filename)s" {0}'
        )
        temp_filename = '{0}.wav'.format(self.temp_filename())
        self.run(command.format(temp_filename) % locals())
        return temp_filename
