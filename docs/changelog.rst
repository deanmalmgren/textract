Change Log
==========

This project uses `semantic versioning <http://semver.org/>`_ to
track version numbers, where backwards incompatible changes
(highlighted in **bold**) bump the major version of the package.


latest changes in development for next release
----------------------------------------------

.. THANKS FOR CONTRIBUTING; MENTION WHAT YOU DID IN THIS SECTION HERE!

* support for ``.rtf`` files (`#84`_)


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

* **standardized encoding of output with ``-e/--encoding`` option**
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
   to make the text above relatively clean

.. _@anthonygarvan: https://github.com/anthonygarvan
.. _@anderser: https://github.com/anderser
.. _@arvindch: https://github.com/arvindch
.. _@christomitov: https://github.com/christomitov
.. _@eiotec: https://github.com/eiotec
.. _@evfredericksen: https://github.com/evfredericksen
.. _@kokxx: https://github.com/Kokxx
.. _@levivm: https://github.com/levivm
.. _@pudo: https://github.com/pudo
.. _@ShawnMilo: https://github.com/ShawnMilo


.. list of issues that have been resolved. putting links here to make
   the text above relatively clean

.. _#2: https://github.com/deanmalmgren/textract/issues/2
.. _#3: https://github.com/deanmalmgren/textract/issues/3
.. _#4: https://github.com/deanmalmgren/textract/issues/4
.. _#6: https://github.com/deanmalmgren/textract/issues/6
.. _#7: https://github.com/deanmalmgren/textract/issues/7
.. _#8: https://github.com/deanmalmgren/textract/issues/8
.. _#9: https://github.com/deanmalmgren/textract/issues/9
.. _#13: https://github.com/deanmalmgren/textract/issues/13
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
.. _#70: https://github.com/deanmalmgren/textract/issues/70
.. _#73: https://github.com/deanmalmgren/textract/issues/73
.. _#76: https://github.com/deanmalmgren/textract/issues/76
.. _#78: https://github.com/deanmalmgren/textract/issues/78
.. _#79: https://github.com/deanmalmgren/textract/issues/79
.. _#82: https://github.com/deanmalmgren/textract/issues/82
.. _#84: https://github.com/deanmalmgren/textract/issues/84
