import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import speech_recognition as sr

from textract.exceptions import UnknownMethod

from .utils import ShellParser

_pocketsphinx = None
_POCKETSPHINX_CODESIGN_ISSUE = False


def _find_pocketsphinx_so() -> Optional[Path]:
    spec = importlib.util.find_spec("pocketsphinx")
    if spec is None or not spec.submodule_search_locations:
        return None
    for loc in spec.submodule_search_locations:
        if matches := list(Path(loc).glob("_pocketsphinx.cpython-*-darwin.so")):
            return matches[0]
    return None


def _pocketsphinx_signature_invalid() -> bool:
    so = _find_pocketsphinx_so()
    if so is None:
        return False
    return (
        subprocess.run(["codesign", "-v", str(so)], capture_output=True).returncode != 0
    )


# On macOS, check code signature before attempting import.
# pocketsphinx built from source (no prebuilt Python 3.14 wheel) has its
# signature invalidated by scikit-build-core's post-build steps, causing
# macOS to send SIGKILL (codesigning violation) when the .so is loaded.
if sys.platform == "darwin" and _pocketsphinx_signature_invalid():
    _POCKETSPHINX_CODESIGN_ISSUE = True
else:
    try:
        import pocketsphinx as _pocketsphinx  # type: ignore[assignment]
    except ImportError:
        pass

_CODESIGN_FIX_MSG = """\
pocketsphinx has an invalid macOS code signature. This happens when the \
package is compiled from source (no prebuilt wheel for this Python version) \
and scikit-build-core's post-build tools invalidate the signature.

Fix with:
  make sync         # if you have the source checked out
  python -c "import subprocess, sys; from pathlib import Path; import importlib.util; spec = importlib.util.find_spec('pocketsphinx'); [subprocess.run(['codesign', '-s', '-', '-f', str(so)]) for loc in (spec.submodule_search_locations or []) for so in Path(loc).glob('_pocketsphinx.cpython-*-darwin.so')]"

See: https://github.com/scikit-build/scikit-build-core/issues for upstream status.\
"""


def _sphinx_transcribe(audio: sr.AudioData) -> str:
    """Transcribe audio using pocketsphinx 5.x with bundled en-US models."""
    if _pocketsphinx is None:
        if _POCKETSPHINX_CODESIGN_ISSUE:
            raise RuntimeError(_CODESIGN_FIX_MSG)
        raise UnknownMethod("sphinx")
    raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
    decoder = _pocketsphinx.Decoder(logfn=os.devnull)
    decoder.start_utt()
    decoder.process_raw(raw_data, no_search=False, full_utt=True)
    decoder.end_utt()
    hyp = decoder.hyp()
    return hyp.hypstr if hyp is not None else ""


class Parser(ShellParser):
    """
    Extract text (i.e. speech) from an audio file, using SpeechRecognition.

    Since SpeechRecognition expects a .wav file, with 1 channel,
    the audio file has to be converted, via sox, if not compliant

    Note: for testing, use -
    http://www2.research.att.com/~ttsweb/tts/demo.php,
    with Rich (US English) for best results
    """

    def extract(self, filename, method="", **kwargs):
        speech = ""

        # convert to wav, if not already .wav
        base, ext = os.path.splitext(filename)
        if ext != ".wav":
            temp_filename = self.convert_to_wav(filename)
            try:
                speech = self.extract(temp_filename, method, **kwargs)
            finally:  # make sure temp_file is deleted
                Path(temp_filename).unlink()
        else:
            r = sr.Recognizer()

            with sr.WavFile(filename) as source:
                audio = r.record(source)

            try:
                if method in {"google", ""}:
                    speech = r.recognize_google(audio)  # type: ignore[attr-defined]
                elif method == "sphinx":
                    speech = _sphinx_transcribe(audio)
                else:
                    raise UnknownMethod(method)
            except LookupError:  # audio is not understandable
                speech = ""
            except sr.UnknownValueError:
                speech = ""
            except sr.RequestError:
                speech = ""

            # add a newline, to make output cleaner
            speech += "\n"

        return speech

    def convert_to_wav(self, filename):
        """
        Uses sox cmdline tool, to convert audio file to .wav

        Note: for testing, use -
        http://www.text2speech.org/,
        with American Male 2 for best results
        """
        temp_filename = f"{self.temp_filename()}.wav"
        self.run(["sox", "-G", "-c", "1", filename, temp_filename])
        return temp_filename
