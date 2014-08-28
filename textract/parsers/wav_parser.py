import speech_recognition as sr

from .utils import BaseParser


class Parser(BaseParser):
    """
    Extract text (i.e. speech) from an audio file, using SpeechRecognition.
    SpeechRecognition expects a .wav file, with one channel
    So the audio file has to be converted, if not compliant
    Note: for testing, use -
    http://www2.research.att.com/~ttsweb/tts/demo.php,
    with Rich (US English) for best results
    """

    def extract(self, filename, **kwargs):
        r = sr.Recognizer()

        with sr.WavFile(filename) as source:
            audio = r.record(source)

        try:
            speech = r.recognize(audio)
        except LookupError:  # audio is not understandable
            speech = ''

        # add a newline, to make output cleaner
        speech += '\n'

        return speech
