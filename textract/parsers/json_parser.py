import json  # noqa: D100
import pathlib

import six

from .utils import BaseParser


class Parser(BaseParser):
    """Extract all of the string values of a json file (no keys as those
    are, in some sense, markup). This is useful for parsing content
    from mongodb dumps, for example.
    """  # noqa: D205

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102
        with pathlib.Path(filename).open(encoding="utf-8") as raw:
            deserialized_json = json.load(raw)
        return self.get_text(deserialized_json)

    def get_text(self, deserialized_json):  # noqa: ANN001, ANN201
        """Recursively get text from subcomponents of a deserialized json. To
        enforce the same order on the documents, make sure to read keys of
        deserialized_json in a consistent (alphabetical) order.
        """  # noqa: D205
        if isinstance(deserialized_json, dict):
            result = ""
            for key in sorted(deserialized_json):
                result += self.get_text(deserialized_json[key]) + " "
            return result

        if isinstance(deserialized_json, list):
            result = ""
            for item in deserialized_json:
                result += self.get_text(item) + " "
            return result

        if isinstance(deserialized_json, six.string_types):
            return deserialized_json
        return ""
