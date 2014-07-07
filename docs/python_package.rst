.. _python-package:

Python package
==============

The core of this package is in the ``textract.parsers`` submodule
organized by file extension. For example, the ``.docx`` parser is
located in ``textract.parsers.docx``. Every parser submodule must have
a method called extract that does the default text extraction for that
file type.

textract.parsers
----------------

.. automodule:: textract.parsers
   :members:


textract.parsers.doc
--------------------

.. automodule:: textract.parsers.doc
   :members:


textract.parsers.docx
---------------------

.. automodule:: textract.parsers.docx
   :members:


textract.parsers.pdf
---------------------

.. automodule:: textract.parsers.pdf
   :members:


textract.parsers.pptx
---------------------

.. automodule:: textract.parsers.pptx
   :members:
