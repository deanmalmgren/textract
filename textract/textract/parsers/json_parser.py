import json

from .utils import BaseParser


class Parser(BaseParser):
    """Extract all of the string values of a json file (no keys as those
    are, in some sense, markup). This is useful for parsing content
    from mongodb dumps, for example.
    """

    def extract(self, filename, **kwargs):
        with open(filename, 'r') as raw:
            deserialized_json = json.load(raw)
        return self.get_text(deserialized_json)

    def get_text(self, deserialized_json):
        """Recursively get text from subcomponents of a deserialized json. To
        enforce the same order on the documents, make sure to read keys of
        deserialized_json in a consistent (alphabetical) order.
        """
        if isinstance(deserialized_json, dict):
            result = ''
            for key in sorted(deserialized_json):
                result += self.get_text(deserialized_json[key]) + ' '
            return result

        if isinstance(deserialized_json, list):
            result = ''
            for item in deserialized_json:
                result += self.get_text(item) + ' '
            return result

        if isinstance(deserialized_json, basestring):
            return deserialized_json
        else:
            return ''
