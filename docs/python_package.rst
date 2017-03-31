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

or to specify a particular output encoding (input encodings are
inferred using `chardet <https://github.com/chardet/chardet>`_)::

    import textract
    text = textract.process('path/to/file.extension', encoding='ascii')

When the file name has no extension, you specify the file's extension as an argument
to ``textract.process`` like this::

    import textract
    text = textract.process('path/to/file', extension='docx')

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

Many of the parsers rely on command line utilities to do some of the
parsing. For convenience, the ``textract.parsers.utils.ShellParser``
class includes some convenience methods for streamlining access to the
command line.

.. autoclass:: textract.parsers.utils.ShellParser
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
