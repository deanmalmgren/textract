changelog
=========

This project uses `semantic versioning <http://semver.org/>`__ to
track version numbers, where backwards incompatible changes
(highlighted in **bold**) bump the major version of the package.


latest
------

[will add changes here as they are made]

* support for ``.json`` files (#13, @anthonygarvan)

* cleaned up implementation of extension parsers.

0.4.0
-----

* support for ``.html`` files (#7)

* support for ``.eml`` files (#4)

* automated the documentation for the python package using
  sphinx-apidoc in docs/Makefile (#9)


0.3.0
-----

* support for ``.txt`` files, haha (#8)

* fixed installation bug with not properly including requirements
  files in the manifest

0.2.0
-----

* support for ``.doc`` files (#2)

* support for ``.pdf`` files (#3)

* several bug fixes, including:

  * fixing tab complete bug no file paths (#6)

  * fixing tests to make sure the work properly on travis-ci

0.1.0
-----

* Initial release, support for ``.docx`` and ``.pptx``
