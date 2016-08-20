import os
import logging

logger = logging.getLogger('textract')

DETECT_METHOD = 'extension'

try:
    import magic
except ImportError:
    magic = None
    logger.warn('Python-magic not detected. Using file extension to detect file type.')


# Dictionary structure for synonymous file extension types
EXTENSION_SYNONYMS = {
    "jpeg": "jpg",
    "htm": "html",
    "": "txt",
}

# Sourced from
# http://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types
MIME_MAPPING = {
    'application/atom+xml': 'txt',
    'application/atomcat+xml': 'txt',
    'application/atomsvc+xml': 'txt',
    'application/ccxml+xml': 'txt',
    'application/davmount+xml': 'txt',
    'application/docbook+xml': 'txt',
    'application/dssc+xml': 'txt',
    'application/ecmascript': 'txt',
    'application/emma+xml': 'txt',
    'application/epub+zip': 'epub',
    'application/gml+xml': 'txt',
    'application/gpx+xml': 'txt',
    'application/inkml+xml': 'txt',
    'application/inkml+xml': 'txt',
    'application/javascript': 'txt',
    'application/json': 'json',
    'application/jsonml+json': 'json',
    'application/lost+xml': 'txt',
    'application/mads+xml': 'txt',
    'application/marcxml+xml': 'txt',
    'application/mathml+xml': 'txt',
    'application/metalink+xml': 'txt',
    'application/metalink4+xml': 'txt',
    'application/mets+xml': 'txt',
    'application/mods+xml': 'txt',
    'application/msword': 'doc',
    'application/ogg': 'ogg',
    'application/pdf': 'pdf',
    'application/postscript': 'ps',
    'application/rdf+xml': 'rdf',
    'application/reginfo+xml': 'txt',
    'application/rss+xml': 'txt',
    'application/rtf': 'rtf',
    'application/sbml+xml': 'txt',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.ms-word.document.macroenabled.12': 'doc',
    'application/vnd.oasis.opendocument.text': 'odt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'application/vnd.openxmlformats-officedocument.presentationml.slide': 'pptx',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'pptx',
    'application/vnd.openxmlformats-officedocument.presentationml.template': 'pptx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template': 'xlsx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'docx',
    'application/xhtml+xml': 'html',
    'application/xml-dtd': 'html',
    'application/xml': 'html',
    'audio/basic': 'audio',
    'audio/midi': 'audio',
    'audio/mp4': 'audio',
    'audio/mpeg': 'audio',
    'audio/ogg': 'ogg',
    'audio/s3m': 'audio',
    'audio/webm': 'audio',
    'audio/x-aac': 'audio',
    'audio/x-flac': 'audio',
    'audio/x-wav': 'wav',
    'image/bmp': 'image',
    'image/cgm': 'image',
    'image/g3fax': 'image',
    'image/gif': 'gif',
    'image/jpeg': 'image',
    'image/png': 'image',
    'image/svg+xml': 'image',
    'image/tiff': 'image',
    'text/calendar': 'txt',
    'text/css': 'txt',
    'text/csv': 'csv',
    'text/html': 'html',
    'text/plain': 'txt',
    'text/richtext': 'rtf',
}


def detect_filetype(filename, default='txt'):
    """
    Detect a file's type, using `default` if not found.
    """
    # First attempt to detect by extension
    _, ext = os.path.splitext(filename)
    if not ext:
        mime = magic.from_file(filename, mime=True)
        ext = MIME_MAPPING.get(mime, default)
        logger.info('File {0} had mimetype {1}'.format(filename, mime))

    logger.info('Using {0} parser'.format(ext))

    # Use the extension synonyms dictionary to consolidate
    ext = ext.lower().strip('.')
    ext = EXTENSION_SYNONYMS.get(ext, ext)
    return ext
