from ExtractMsg import Message

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from Microsoft Outlook files (.msg)
    """

    def extract(self, filename, **kwargs):
        m = Message(filename)
        return m.subject + '\n\n' + m.body
