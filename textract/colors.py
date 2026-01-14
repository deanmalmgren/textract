"""Inspiration from
https://github.com/fabric/fabric/blob/master/fabric/colors.py.
"""  # noqa: D205

import re


def _wrap_with(code, bold=False):  # noqa: ANN001, ANN202, FBT002
    def inner(text) -> str:  # noqa: ANN001
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

bold_red = _wrap_with("31", True)  # noqa: FBT003
bold_green = _wrap_with("32", True)  # noqa: FBT003
bold_yellow = _wrap_with("33", True)  # noqa: FBT003
bold_blue = _wrap_with("34", True)  # noqa: FBT003
bold_magenta = _wrap_with("35", True)  # noqa: FBT003
bold_cyan = _wrap_with("36", True)  # noqa: FBT003
bold_white = _wrap_with("37", True)  # noqa: FBT003


# regular expression to omit colorcodes
def colorless(text):  # noqa: ANN001, ANN201
    """Remove color from the text."""
    return re.sub(r"\033\[(1;)?[\d]+m", "", text)
