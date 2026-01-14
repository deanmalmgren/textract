import pathlib  # noqa: D100
from email.parser import Parser as EmailParser

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from email messages in .eml format. This gets the
    subject and all text from the contents.
    """  # noqa: D205

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102, PLR6301
        # TODO: could make option here to omit all non-original content
        # (forwarded content, quoted content in reply, signature, etc),
        # perhaps using https://github.com/zapier/email-reply-parser

        # TODO: could also potentially grab text/html content instead of
        # only grabbing text/plain content

        with pathlib.Path(filename).open(encoding="utf-8") as stream:
            parser = EmailParser()
            message = parser.parse(stream)

        text_content = [
            str(part.get_payload())
            for part in message.walk()
            if part.get_content_type().startswith("text/plain")
        ]
        return "\n\n".join(text_content)
