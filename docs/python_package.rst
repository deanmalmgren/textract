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

