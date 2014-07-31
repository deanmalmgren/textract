from ..MsgExtractor import Message


def extract(filename, **kwargs):
    """Extract microsoft outlook .msg email file format. Includes the subject
    and body of the message, but no attachments.
    """
    m = Message(filename)
    return m.subject + '\n' + m.body
