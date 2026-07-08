.. _python-package:

Python package
==============

This package is organized to make it as easy as possible to add new
extensions and support the continued growth and coverage of
textract. For almost all applications, you will just have to do
something like this::

    import textract
    text = textract.process('path/to/file.extension')

to obtain text from a document. You can also pass keyword arguments to
``textract.process``, for example, to use a particular method for
parsing a pdf like this::

    import textract
    text = textract.process('path/to/a.pdf', method='pdfminer')

or to specify a particular output encoding::

    import textract
    text = textract.process('path/to/file.extension', encoding='ascii')

By default, input encodings are inferred using `chardet
<https://github.com/chardet/chardet>`_. For parsers that consume decoded
text (csv, eml, html, json), you can override this and specify the
input file's encoding explicitly, which is useful when chardet's
guess is wrong or its confidence is too low (e.g. for short files)::

    import textract
    text = textract.process('path/to/file.csv', input_encoding='cp1251')

The same option is available on the command line as ``--input-encoding``.
If ``input_encoding`` doesn't match the file's actual encoding, a
:class:`textract.exceptions.InvalidInputEncoding` error is raised
rather than silently producing corrupted text.

When the file name has no extension, you specify the file's extension as an argument
to ``textract.process`` like this::

    import textract
    text = textract.process('path/to/file', extension='docx')

.. _beta-in-memory-input:

Beta: in-memory and streamed input
-----------------------------------

If you already have the document's bytes in memory (e.g. an HTTP response
body) rather than a path on disk, ``process_bytes`` skips writing your own
temp file::

    import requests
    import textract

    response = requests.get('https://example.com/report.pdf')
    text = textract.process_bytes(response.content, extension='pdf')

For a readable binary stream (a socket, an open file object, ``sys.stdin.
buffer``), ``process_stream`` works the same way::

    import textract

    with open('path/to/file.docx', 'rb') as stream:
        text = textract.process_stream(stream, extension='docx')

Both require ``extension`` explicitly, since there's no filename to detect
it from; omitting it raises :class:`textract.exceptions.ExtensionRequired`.
Both also emit a ``FutureWarning`` since this API is still beta and may
change.

For csv specifically, passing ``input_encoding`` lets textract read and
decode the input lazily line-by-line instead of buffering the whole
document in memory first (this is also what powers the CLI's ``-i``/
``--input-encoding`` flag with ``-`` stdin, see
:ref:`command-line-interface`)::

    import textract

    with open('path/to/huge.csv', 'rb') as stream:
        text = textract.process_stream(stream, extension='csv', input_encoding='utf_8')

Other formats don't have a streaming implementation yet and still buffer
the whole input regardless of ``input_encoding``. See the "Next steps"
note in ``tests/test_source_input.py`` for what's left.

.. _additional-options:

Additional options
------------------

Some parsers also enable additional options which can be passed in as keyword
arguments to the ``textract.process`` function. Here is a quick table of
available options that are available to the different types of parsers:

======  =========  ===========================================================
parser  option     description
======  =========  ===========================================================
gif     language   Specify `the language`_ for OCR-ing text with tesseract
jpg     language   Specify `the language`_ for OCR-ing text with tesseract
pdf     language   For use when ``method='tesseract'``, specify `the language`_
pdf     layout     With ``method='pdftotext'`` (default), preserve the layout
png     language   Specify `the language`_ for OCR-ing text with tesseract
tiff    language   Specify `the language`_ for OCR-ing text with tesseract
======  =========  ===========================================================

As an example of using these additional options, you can extract text from a
Norwegian PDF using Tesseract OCR like this::

    text = textract.process(
        'path/to/norwegian.pdf',
        method='tesseract',
        language='nor',
    )


A look under the hood
---------------------

When ``textract.process('path/to/file.extension')`` is called,
``textract.process`` looks for a module called
``textract.parsers.extension_parser`` that also contains a ``Parser``.


.. autofunction:: textract.parsers.process

Importantly, the ``textract.parsers.extension_parser.Parser`` class
must inherit from ``textract.parsers.utils.BaseParser``.

.. autoclass:: textract.parsers.utils.BaseParser
    :members:
    :undoc-members:
    :show-inheritance:

Whatever the caller passed in (a filename, ``bytes``, or a stream) is
normalized into a single ``textract.parsers.utils.Source`` before reaching
a parser, so parsers don't have to own file I/O themselves. A parser
declares which form it needs by which of ``BaseParser``'s three
input-kind subclasses it inherits from.

.. autoclass:: textract.parsers.utils.Source
    :members:
    :undoc-members:

Many of the parsers rely on command line utilities to do some of the
parsing. For convenience, the ``textract.parsers.utils.ShellParser``
class (a kind of ``PathParser``, see below) includes some convenience
methods for streamlining access to the command line.

.. autoclass:: textract.parsers.utils.PathParser
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: textract.parsers.utils.ShellParser
    :members:
    :undoc-members:
    :show-inheritance:

Parsers with a native Python implementation that consume decoded text
rather than a filename (csv, eml, html, json) can instead inherit from
``textract.parsers.utils.DecodedParser``, which reads and decodes the
file (honoring ``input_encoding``) before handing the text to
:meth:`.DecodedParser.extract_from_text`.

.. autoclass:: textract.parsers.utils.DecodedParser
    :members:
    :undoc-members:
    :show-inheritance:

**Beta:** parsers whose underlying library can consume raw bytes or a
file-like object directly (e.g. docx/xlsx/pptx/epub opening a zip) can
instead inherit from ``textract.parsers.utils.BytesParser``, which never
needs a temp file.

.. autoclass:: textract.parsers.utils.BytesParser
    :members:
    :undoc-members:
    :show-inheritance:


A few specific examples
-----------------------

There are quite a few parsers included with ``textract``. Rather than
elaborating all of them, here are a few that demonstrate how parsers
work.

.. autoclass:: textract.parsers.epub_parser.Parser
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: textract.parsers.doc_parser.Parser
    :members:
    :undoc-members:
    :show-inheritance:


.. _the language: https://code.google.com/p/tesseract-ocr/downloads/list
