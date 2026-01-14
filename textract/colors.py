"""Inspiration from
https://github.com/fabric/fabric/blob/master/fabric/colors.py.
"""

import re


def _wrap_with(code, bold=False):
    def inner(text) -> str:
        c = code
        if bold:
            c = f"1;{c}"
        return f"\033[{c}m{text}\033[0m"

    return inner


red = _wrap_with("31")
green = _wrap_with("32")
yellow = _wrap_with("33")
blue = _wrap_with("34")
magenta = _wrap_with("35")
cyan = _wrap_with("36")
white = _wrap_with("37")

bold_red = _wrap_with("31", True)
bold_green = _wrap_with("32", True)
bold_yellow = _wrap_with("33", True)
bold_blue = _wrap_with("34", True)
bold_magenta = _wrap_with("35", True)
bold_cyan = _wrap_with("36", True)
bold_white = _wrap_with("37", True)


# regular expression to omit colorcodes
def colorless(text):
    """Remove color from the text."""
    return re.sub(r"\033\[(1;)?[\d]+m", "", text)
