from email.parser import Parser as EmailParser
from pathlib import Path

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from email messages in .eml format. This gets the
    subject and all text from the contents.
    """

    def extract(self, filename, input_encoding=None, **kwargs):
        # TODO: could make option here to omit all non-original content
        # (forwarded content, quoted content in reply, signature, etc),
        # perhaps using https://github.com/zapier/email-reply-parser

        # TODO: could also potentially grab text/html content instead of
        # only grabbing text/plain content

        raw_bytes = Path(filename).read_bytes()
        text = self.decode(raw_bytes, input_encoding)
        message = EmailParser().parsestr(text)

        text_content = [
            str(part.get_payload())
            for part in message.walk()
            if part.get_content_type().startswith("text/plain")
        ]
        return "\n\n".join(text_content)
