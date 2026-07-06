.. _command-line-interface:

Command line interface
======================

textract
--------

.. argparse::
   :module: textract.cli
   :func: get_parser
   :prog: textract

.. note::

    To make the command line interface as usable as possible,
    autocompletion of available options with textract is enabled by
    @kislyuk's amazing `argcomplete
    <https://github.com/kislyuk/argcomplete>`_ package.  Follow
    instructions to `enable global autocomplete
    <https://github.com/kislyuk/argcomplete#activating-global-completion>`_
    and you should be all set.

.. note::

    **Beta:** pass ``-`` as the filename to read the document from stdin
    instead of a file on disk, so textract works as a pipe::

        curl https://example.com/report.pdf | textract --extension pdf -

    Since there's no filename to sniff the extension from, ``--extension``
    is required. For csv, adding ``--input-encoding`` also lets textract
    read and decode the input lazily instead of buffering the whole
    document, so a large piped csv doesn't need to be fully loaded before
    processing starts::

        cat huge.csv | textract --extension csv --input-encoding utf_8 -

    This currently only holds for csv; other formats still buffer the
    document. See :ref:`python-package` for the equivalent library
    functions (``process_bytes``, ``process_stream``) and their current
    limitations.
