import speech_recognition as sr

from .utils import BaseParser


class Parser(BaseParser):
    """
    Extract text (i.e. speech) from an audio file, using SpeechRecognition.
    Only works with .wav files, for now.
    """

    def extract(self, filename, **kwargs):
        r = sr.Recognizer()

        with sr.WavFile(filename) as source:
            audio = r.record(source)

        try:
            speech = r.recognize(audio)
        except LookupError:
            speech = 'Could not understand audio.'

        return speech
