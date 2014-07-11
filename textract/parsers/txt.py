def extract(filename, **kwargs):
    """Extract text from a .txt file
    """
    with open(filename) as stream:
        return stream.read()
