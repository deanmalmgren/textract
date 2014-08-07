Change Log
==========

This project uses `semantic versioning <http://semver.org/>`__ to
track version numbers, where backwards incompatible changes
(highlighted in **bold**) bump the major version of the package.


latest changes in development
-----------------------------

[will add changes here as they are made]

0.5.0
-----

* support for ``.json`` files (`#13`_ via `@anthonygarvan`_)

* support for ``.odt`` files (`#29`_ via `@christomitov`_)

* support for ``.ps`` files (`#25`_)

* support for ``.gif``, ``.jpg``, ``.jpeg``, and ``.png`` files
  (`#30`_ via `@christomitov`_)

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
.. _@christomitov: https://github.com/christomitov


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

