import os  # noqa: D100
import pathlib

import speech_recognition as sr

from textract.exceptions import UnknownMethod

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text (i.e. speech) from an audio file, using SpeechRecognition.

    Since SpeechRecognition expects a .wav file, with 1 channel,
    the audio file has to be converted, via sox, if not compliant

    Note: for testing, use -
    http://www2.research.att.com/~ttsweb/tts/demo.php,
    with Rich (US English) for best results
    """

    def extract(self, filename, method="", **kwargs):  # noqa: ANN001, ANN201, D102
        speech = ""

        # convert to wav, if not already .wav
        _base, ext = os.path.splitext(filename)  # noqa: PTH122
        if ext != ".wav":
            temp_filename = self.convert_to_wav(filename)
            try:
                speech = self.extract(temp_filename, method, **kwargs)
            finally:  # make sure temp_file is deleted
                pathlib.Path(temp_filename).unlink()
        else:
            r = sr.Recognizer()

            with sr.WavFile(filename) as source:
                audio = r.record(source)

            try:
                if method in {"google", ""}:
                    speech = r.recognize_google(audio)  # type: ignore[attr-defined]
                elif method == "sphinx":
                    speech = r.recognize_sphinx(audio)  # type: ignore[attr-defined]
                else:
                    raise UnknownMethod(method)
            except LookupError:  # audio is not understandable
                speech = ""
            except sr.UnknownValueError:
                speech = ""

            # add a newline, to make output cleaner
            speech += "\n"

        return speech

    def convert_to_wav(self, filename):  # noqa: ANN001, ANN201
        """Uses sox cmdline tool, to convert audio file to .wav.

        Note: for testing, use -
        http://www.text2speech.org/,
        with American Male 2 for best results
        """
        temp_filename = f"{self.temp_filename()}.wav"
        self.run(["sox", "-G", "-c", "1", filename, temp_filename])
        return temp_filename
