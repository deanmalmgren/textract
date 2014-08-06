.. textract documentation master file, created by
   sphinx-quickstart on Fri Jul  4 11:09:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

textract
================================

As undesireable as it might be, more often than not there is extremely
useful information embedded in Word documents, PowerPoint
presentations, PDFs, etc---so-called "dark data"---that would be
valuable for further textual analysis and visualization. While
:ref:`several packages <supporting>` exist for extracting content from
each of these formats on their own, this package provides a single
interface for extracting content from any type of file, without any
irrelevant markup.

This package provides two primary facilities for doing this, the
:ref:`command line interface <command-line-interface>`

.. code-block:: bash

    textract path/to/file.extension

or the :ref:`python package <python-package>`

.. code-block:: python

    # some python file
    import textract
    text = textract.process("path/to/file.extension")

.. _supporting:

Currently supporting
--------------------

* ``.doc`` via `antiword <http://www.winfield.demon.nl/>`__

* ``.docx`` via `python-docx <https://python-docx.readthedocs.org/en/latest/>`__

* ``.eml`` via python builtins

* ``.json`` via python builtins

* ``.html`` via `beautifulsoup4 <http://beautiful-soup-4.readthedocs.org/en/latest/>`__

* ``.odt`` via python builtins

* ``.pptx`` via `python-pptx <https://python-pptx.readthedocs.org/en/latest/>`__

* ``.pdf`` via `pdftotext <http://poppler.freedesktop.org/>`__ (default) or `pdfminer <https://euske.github.io/pdfminer/>`__

* ``.ps`` via `ps2text <http://pages.cs.wisc.edu/~ghost/doc/pstotext.htm>`__

* ``.txt`` via python builtins

Please recommend other file types by either mentioning them on the
`issue tracker <https://github.com/deanmalmgren/textract/issues>`__ or
by :ref:`contributing <contributing>`


.. _related-projects:

Related projects
----------------

Of course, textract isn't the first project with the aim to provide a
simple interface for extracting text from any document. But this is,
to the best of my knowledge, the only project that is written in
python (a language commonly chosen by the natural language processing
community) and is method agnostic about how content is extracted (more
on this :ref:`here <contributing>`). Here is a small sample of similar
projects (feel free to add to the list):

* `Apache Tika <http://tika.apache.org/>`__ has `very similar, if not
  identical, aims as textract
  <https://github.com/deanmalmgren/textract/issues/12>`__. It has
  impressive coverage of a wide range of file formats and is written
  in java.

* `textract (node.js) <https://github.com/dbashford/textract>`__ has
  similar aims as this textract package (including an identical name!
  great minds...). It is written in node.js.


Contents:

.. toctree::
   :maxdepth: 2

   command_line_interface
   python_package
   installation
   contributing
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

