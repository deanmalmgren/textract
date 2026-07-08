Known Platform Differences
===========================

``textract`` shells out to third-party tools (Poppler, Ghostscript, sox,
tesseract) to extract text from binary formats. Those tools are installed
via different package managers per OS in CI (apt on Linux, brew on macOS,
choco on Windows), and their builds don't always produce byte-identical
output for the same input file: line-wrap width, whitespace padding, and
even punctuation glyphs (curly vs straight quotes) can vary by version.

The table below is generated from a single registry
(``tests/platform_limitations.py``) that the test suite's ``xfail``/
``skip`` markers also read from, so this list and the actual test
behavior can't silently drift apart
(enforced by ``tests/test_platform_limitations.py``).

.. list-table::
   :header-rows: 1
   :widths: 20 15 45 20

   * - Format
     - Platform
     - Known difference
     - Covered by
   * - MP3
     - Windows
     - sox.portable on Windows lacks libmad for MP3 decoding
     - ``tests/test_mp3.py::Mp3TestCase``
   * - PDF
     - Windows
     - PDF content may differ on Windows
     - ``tests/test_pdf.py::PdfTestCase``,
       ``tests/test_source_input.py::SourceInputTestCase::test_cli_stdin``
   * - PDF (tesseract OCR)
     - Linux (CI)
     - Tesseract OCR output varies by version; Linux CI has different output
     - ``tests/test_pdf.py::PdfTestCase::test_method_python/test_method_cli``
   * - PostScript (.ps)
     - Windows
     - PS text layout may differ between gswin64c txtwrite and ps2ascii
     - ``tests/test_ps.py::PsTestCase``

If your use case depends on byte-exact output across platforms, pin the
extraction to a single OS, or normalize whitespace/punctuation on your
side the way ``tests/base.py``'s ``dewrap()`` helper does for the test
suite itself.
