import six

import extract_msg

from .utils import BaseParser


def ensure_bytes(string):
    """Normalize string to bytes.

    `ExtractMsg.Message._getStringStream` can return unicode or bytes depending
    on what is originally stored in message file.

    This helper functon makes sure, that bytes type is returned.
    """
    if isinstance(string, six.string_types):
        return string.encode('utf-8')
    return string


class Parser(BaseParser):
    """Extract text from Microsoft Outlook files (.msg)
    """

    def extract(self, filename, **kwargs):
        m = extract_msg.Message(filename)
        return ensure_bytes(m.subject) + six.b('\n\n') + ensure_bytes(m.body)
