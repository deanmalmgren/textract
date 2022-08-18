Change Log
==========

This project uses `semantic versioning <http://semver.org/>`_ to
track version numbers, where backwards incompatible changes
(highlighted in **bold**) bump the major version of the package.


latest changes in development for next release
----------------------------------------------

.. THANKS FOR CONTRIBUTING; ADD YOUR UNRELEASED CHANGES HERE!
1.7.0
-------------------

* Dropped python2 support

1.6.5
-------------------

* switched epub parsing to MIT license compatible package (`#411`_ by
  `@jhale1805`_)

1.6.4
-------------------

* several bug fixes, including:

  * fixing dependency declarations (`#162`_ by `@lillypad`_)


1.6.1
-------------------

* several bug fixes, including:

  * fixing the readthedocs build (`#150`_)


1.6.0
-------------------

* Let the user provide file extension as an argument when the file name has no
  extension (`#148`_ by `@motazsaad`_)

* Added ability to parse audio with ``pocketsphinx`` (`#122`_ by `@barrust`_)

* Added ability to parse ``.psv`` and ``.tsv`` files (`#141`_)

* several bug fixes, including:

  * checking for the importability of a parser rather than the presense of the
    file (`#136`_ by `@AusIV`_)

  * manage versions with `bumpversion <https://pypi.python.org/pypi/bumpversion>`_
    (`#146`_)

  * properly reporting on missing external dependencies (`#139`_ by `@AusIV`_)

  * pin `chardet` to version 2.1.1 to avoid decode errors (`#107`_)

  * avoid unicode decode error with html parser (`#147`_ by `@suned`_)

  * enabling autocomplete and improving error handling (`#149`_)

1.5.0
-----

* Added python 3 support, including pdfminer (`#104`_ by `@sirex`_ via `#126`_)

* Python 3 support for ``pdfminer`` using ``pdfminer.six`` (`#116`_ by
  `@jaraco`_ via `#126`_)

* fixed security vulnerability by properly using subprocess.call (`#114`_ by
  `@pierre-ernst`_)

* updating to ``tesseract`` 3.03 (`#127`_)

* adding a ``.tif`` synonym for ``.tiff`` files (`#113`_ by `@onionradish`_)

* improved ``.docx`` support using ``docx2txt`` (`#100`_ by `@ankushshah89`_)

* several bug fixes, including:

  * including all requirements for ``Pillow`` (`#119`_ by `@akoumjian`_)

1.4.0
-----

* added layout preservation option for pdftotext pdf extractor (`#93`_ by
  `@ankushshah89`_)

* added simple support for extensionless filenames, treating them as plain
  ``.txt`` files (`#85`_)

* several bug fixes, including:

  * now extracting the text in tables from docx files at the end of the text
    extraction (`#92`_ by `@jsmith-mploir`_)

  * faster testing framework by only rebuilding test data when needed (`#90`_)

  * fixed ``.html`` and ``.epub`` parsers to deal with beautifulsoup4
    upgrades

  * using official ``msg-extractor`` now that it has a native ``setup.py``

  * updated tests for ``.html``, ``.ogg``, ``.wav``, and ``.mp3`` file types to
    be consistent with more recent versions of the underlying packages.


1.3.0
-----

* support for ``.rtf`` files (`#84`_)

* support for ``.msg`` files (`#87`_ and `#17`_ by `@anthonygarvan`_)


1.2.0
-----

* support for ``.tiff`` files (`#81`_)

* added support for other languages for tesseract (`#76`_ by `@anderser`_)

* added ``--option/-O`` flag to pass arbitrary arguments for things like
  languages into textract

* several bug fixes, including:

  * fix bug with doing OCR on multi-page pdfs and removing temporary directory
    (`#82`_ by `@pudo`_)

  * correctly accounting for whitespace in ``.odt`` documents (`#79`_
    by `@evfredericksen`_)

  * standardizing testing environment to be compatible with different versions
    of third-party command line tools (`#78`_)


1.1.0
-----

* support for ``.wav``, ``.mp3``, and ``.ogg`` files (`#56`_ and
  `#62`_ by `@arvindch`_)

* support for ``.csv`` files (`#64`_)

* support for scanned ``.pdf`` files with tesseract (`#66`_ by
  `@pudo`_)

* support for ``.htm`` files (`#69`_)

* several bug fixes, including:

  * ``.odt`` parser now correctly extracts text in order (`#61`_ by
    `@levivm`_)

  * fixed Docker development environment compatability with the
    Vagrant VM environment (`#73`_ by `@ShawnMilo`_)

* several internal improvements, including:

  * improvements in the python documentation (`#70`_)

  * improved html output with reduced whitespace around inline
    elements in output text (`#58`_ by `@eiotec`_)


1.0.0
-----

* **standardized encoding of output with** ``-e/--encoding`` **option**
  (`#39`_)

* support for ``.xls`` and ``.xlsx`` files (`#42`_ and `#55`_ by `@levivm`_)

* support for ``.epub`` files (`#40`_ by `@kokxx`_)

* several bug fixes, including:

  * removing tesseract version info from output of image parsers
    (`#48`_)

  * problems with spaces in filenames (`#53`_)

  * concurrancy problems with tesseract (`#44`_ by `@ShawnMilo`_,
    `#41`_ by `@christomitov`_)

* several internal improvements, including:

  * switching to using class-based parsers to abstract away the common
    functionality between different parser classes (`#39`_)

  * switching to using a python-based test suite and added
    standardized text tests to make sure output is consistent across
    file types (`#49`_)

  * including support for Docker-based testing (`#46`_ by `@ShawnMilo`_)


0.5.1
-----

* several bug fixes, including:

  * documentation fixes

  * shell commands hanging on large files (`#33`_)


0.5.0
-----

* support for ``.json`` files (`#13`_ by `@anthonygarvan`_)

* support for ``.odt`` files (`#29`_ by `@christomitov`_)

* support for ``.ps`` files (`#25`_)

* support for ``.gif``, ``.jpg``, ``.jpeg``, and ``.png`` files
  (`#30`_ by `@christomitov`_)

* several bug fixes, including:

  * improved fallback handling in ``.pdf`` parser if the ``pdftotext``
    command line utility isn't installed (`#26`_)

  * improved documentation for installation instructions on non-Ubuntu
    operating systems (`#21`_, `#26`_)

* several internal improvements, including:

  * cleaned up implementation of extension parsers to avoid magic


0.4.0
-----

* support for ``.html`` files (`#7`_)

* support for ``.eml`` files (`#4`_)

* automated the documentation for the python package using
  sphinx-apidoc in docs/Makefile (`#9`_)


0.3.0
-----

* support for ``.txt`` files, haha (`#8`_)

* fixed installation bug with not properly including requirements
  files in the manifest


0.2.0
-----

* support for ``.doc`` files (`#2`_)

* support for ``.pdf`` files (`#3`_)

* several bug fixes, including:

  * fixing tab complete bug no file paths (`#6`_)

  * fixing tests to make sure the work properly on travis-ci


0.1.0
-----

* Initial release, support for ``.docx`` and ``.pptx``


.. list of contributors that are linked to above. putting links here
.. to make the text above relatively clean

.. _@akoumjian: https://github.com/akoumjian
.. _@anthonygarvan: https://github.com/anthonygarvan
.. _@anderser: https://github.com/anderser
.. _@ankushshah89: https://github.com/ankushshah89
.. _@arvindch: https://github.com/arvindch
.. _@barrust: https://github.com/barrust
.. _@AusIV: https://github.com/AusIV
.. _@christomitov: https://github.com/christomitov
.. _@eiotec: https://github.com/eiotec
.. _@evfredericksen: https://github.com/evfredericksen
.. _@jaraco: https://github.com/jaraco
.. _@jhale1805: https://github.com/jhale1805
.. _@jsmith-mploir: https://github.com/jsmith-mploir
.. _@kokxx: https://github.com/Kokxx
.. _@levivm: https://github.com/levivm
.. _@lillypad: https://github.com/lillypad
.. _@motazsaad: https://github.com/motazsaad
.. _@onionradish: https://github.com/onionradish
.. _@pierre-ernst: https://github.com/pierre-ernst
.. _@pudo: https://github.com/pudo
.. _@ShawnMilo: https://github.com/ShawnMilo
.. _@sirex: https://github.com/sirex
.. _@suned: https://github.com/suned


.. list of issues that have been resolved. putting links here to make
.. the text above relatively clean

.. _#2: https://github.com/deanmalmgren/textract/issues/2
.. _#3: https://github.com/deanmalmgren/textract/issues/3
.. _#4: https://github.com/deanmalmgren/textract/issues/4
.. _#6: https://github.com/deanmalmgren/textract/issues/6
.. _#7: https://github.com/deanmalmgren/textract/issues/7
.. _#8: https://github.com/deanmalmgren/textract/issues/8
.. _#9: https://github.com/deanmalmgren/textract/issues/9
.. _#13: https://github.com/deanmalmgren/textract/issues/13
.. _#17: https://github.com/deanmalmgren/textract/issues/17
.. _#21: https://github.com/deanmalmgren/textract/issues/21
.. _#25: https://github.com/deanmalmgren/textract/issues/25
.. _#26: https://github.com/deanmalmgren/textract/issues/26
.. _#29: https://github.com/deanmalmgren/textract/issues/29
.. _#30: https://github.com/deanmalmgren/textract/issues/30
.. _#33: https://github.com/deanmalmgren/textract/issues/33
.. _#39: https://github.com/deanmalmgren/textract/issues/39
.. _#40: https://github.com/deanmalmgren/textract/issues/40
.. _#41: https://github.com/deanmalmgren/textract/issues/41
.. _#42: https://github.com/deanmalmgren/textract/issues/42
.. _#44: https://github.com/deanmalmgren/textract/issues/44
.. _#46: https://github.com/deanmalmgren/textract/issues/46
.. _#48: https://github.com/deanmalmgren/textract/issues/48
.. _#49: https://github.com/deanmalmgren/textract/issues/49
.. _#53: https://github.com/deanmalmgren/textract/issues/53
.. _#55: https://github.com/deanmalmgren/textract/issues/55
.. _#56: https://github.com/deanmalmgren/textract/issues/56
.. _#58: https://github.com/deanmalmgren/textract/issues/58
.. _#61: https://github.com/deanmalmgren/textract/issues/61
.. _#62: https://github.com/deanmalmgren/textract/issues/62
.. _#64: https://github.com/deanmalmgren/textract/issues/64
.. _#66: https://github.com/deanmalmgren/textract/issues/66
.. _#69: https://github.com/deanmalmgren/textract/issues/69
.. _#70: https://github.com/deanmalmgren/textract/issues/70
.. _#73: https://github.com/deanmalmgren/textract/issues/73
.. _#76: https://github.com/deanmalmgren/textract/issues/76
.. _#78: https://github.com/deanmalmgren/textract/issues/78
.. _#79: https://github.com/deanmalmgren/textract/issues/79
.. _#81: https://github.com/deanmalmgren/textract/issues/81
.. _#82: https://github.com/deanmalmgren/textract/issues/82
.. _#84: https://github.com/deanmalmgren/textract/issues/84
.. _#85: https://github.com/deanmalmgren/textract/issues/85
.. _#87: https://github.com/deanmalmgren/textract/issues/87
.. _#90: https://github.com/deanmalmgren/textract/issues/90
.. _#92: https://github.com/deanmalmgren/textract/issues/92
.. _#93: https://github.com/deanmalmgren/textract/issues/93
.. _#100: https://github.com/deanmalmgren/textract/issues/100
.. _#104: https://github.com/deanmalmgren/textract/issues/104
.. _#107: https://github.com/deanmalmgren/textract/issues/107
.. _#113: https://github.com/deanmalmgren/textract/issues/113
.. _#114: https://github.com/deanmalmgren/textract/issues/114
.. _#116: https://github.com/deanmalmgren/textract/issues/116
.. _#119: https://github.com/deanmalmgren/textract/issues/119
.. _#126: https://github.com/deanmalmgren/textract/issues/126
.. _#122: https://github.com/deanmalmgren/textract/issues/122
.. _#127: https://github.com/deanmalmgren/textract/issues/127
.. _#136: https://github.com/deanmalmgren/textract/issues/136
.. _#139: https://github.com/deanmalmgren/textract/issues/139
.. _#141: https://github.com/deanmalmgren/textract/issues/141
.. _#146: https://github.com/deanmalmgren/textract/issues/146
.. _#147: https://github.com/deanmalmgren/textract/issues/147
.. _#148: https://github.com/deanmalmgren/textract/issues/148
.. _#149: https://github.com/deanmalmgren/textract/issues/149
.. _#150: https://github.com/deanmalmgren/textract/issues/150
.. _#162: https://github.com/deanmalmgren/textract/issues/162
.. _#411: https://github.com/deanmalmgren/textract/issues/411
