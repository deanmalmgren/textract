from email.parser import Parser as EmailParser

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from email messages in .eml format. This gets the
    subject and all text from the contents.
    """

    def extract(self, filename, **kwargs):
        # TODO: could make option here to omit all non-original content
        # (forwarded content, quoted content in reply, signature, etc),
        # perhaps using https://github.com/zapier/email-reply-parser

        # TODO: could also potentially grab text/html content instead of
        # only grabbing text/plain content

        with open(filename) as stream:
            parser = EmailParser()
            message = parser.parse(stream)

        text_content = []
        for part in message.walk():
            if part.get_content_type().startswith('text/plain'):
                text_content.append(part.get_payload())
        return '\n\n'.join(text_content)
