Any and all contributions are welcome and appreciated. To make it easy
to keep things organized, this project uses the
[general guidelines](https://help.github.com/articles/using-pull-requests)
for the fork-branch-pull request model for github. Briefly, this means:

1. Make sure your fork's `master` branch is up to date:

    	git remote add deanmalmgren https://github.com/deanmalmgren/textract.git
        git checkout master
        git pull deanmalmgren/master

2. Start a feature branch with a descriptive name about what you're
   trying to accomplish:

        git checkout -b csv-support

3. Make commits in a way that other people can understand with good
   commit messages to explain the changes you've made:

        emacs -nw textract/parsers/csv_parser.py
	    git add textract/parsers/csv_parser.py
	    git commit -am 'added csv_parser'

4. If an issue already exists for the code you're contributing, use
   [issue2pr](http://issue2pr.herokuapp.com/) to attach your code to
   that issue:

        git push origin csv-support
		chrome http://issue2pr.herokuapp.com
		# enter the issue URL, HEAD=yourusername:csv-support, Base=master

   If the issue doesn't already exist, just send a pull
   request in the usual way:

        git push origin csv-support
		chrome http://github.com/deanmalmgren/textract/compare


Common contributions: support for new file type
-----------------------------------------------

This project has really taken off, much more so than I would have
thought (thanks everybody!). To help new contributors, I thought I'd
jot down some notes for one of the more common contributions---how to
add support for hitherto unsupported file type `.abc123`:

* write an `extract` function in `textract/parsers/abc123_parser.py`

* add a test file in `tests/abc123/some_filename_that_you_like.abc123`

* add your test file to the functional test suite in
  `tests/run_functional_tests.sh` and make sure your test runs
  correctly (you'll probably need to specify the correct md5 checksum,
  which should be pretty obvious after you run the script the first
  time).

* if your package relies on any external sources, be sure to add them
  in either `requirements/python` (for python packages) or
  `requirements/debian` (for debian packages) and update the
  installation documentation accordingly in `docs/installation.rst`.

* add documentation about the awesome new file format this is being
  supported in `docs/index.rst` and be sure to give yourself a pat on
  the back by updating the changelog in `docs/changelog.rst`

* finally, make sure the entire test suite passes by running
  `./tests/run.py` and fix any lingering problems.


Style guidelines
----------------

As a general rule of thumb, the goal of this package is to be as
readable as possible to make it easy for novices and experts alike to
contribute to the source code in meaningful ways. Pull requests that
favor cleverness or optimization over readability are less likely to be
incorporated.

To make this notion of "readability" more concrete, here are a few
stylistic guidelines that we recommend:

-  write functions and methods that can `fit on a screen or two of a
   standard
   terminal <https://www.kernel.org/doc/Documentation/CodingStyle>`_
   --- no more than approximately 40 lines.

-  unless it makes code less readable, adhere to `PEP
   8 <http://legacy.python.org/dev/peps/pep-0008/>`_ style
   recommendations --- use an appropriate amount of whitespace.

-  `code comments should be about *what* is being done, not *how* it is
   being done <https://www.kernel.org/doc/Documentation/CodingStyle>`_
   --- that should be self-evident from the code itself.

Testing with Docker
-------------------

**TL;DR;**

Just run `requirements/run_docker_tests.sh` and it should work.

**Installing Docker on Ubuntu**

Go to the [Docker documentation](http://docs.docker.com/installation/ubuntulinux/)
and follow the instructions under "If you'd like to try the latest version of Docker:"
