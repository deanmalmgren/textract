Any and all contributions are welcome and appreciated. To make it easy
to keep things organized, this project uses the
[general guidelines](https://help.github.com/articles/using-pull-requests)
for the fork-branch-pull request model for github.

### Reporting bugs

If you observe an unexpected behavior, tasks being re-run when they
shouldn't be, suspicious output, etc, one of the simplest ways of
reporting the bug is to [create a gist](https://gist.github.com/) with
any relevant source code that is necessary for reproducing the issue. 
Another possibility is to execute `flo archive` to create a tarball 
with the offending code and share a dropbox link or put it in a gist as well.

### Contributing to the source code

As a general rule of thumb, the goal of this package is to be as
readable as possible to make it easy for novices and experts alike to
contribute to the source code in meaningful ways. Pull requests that
favor cleverness or optimization over readability are less likely to
be incorporated into the source code.

To make this notion of "readability" more concrete, here are a few
stylistic guidelines that were implemented:

* write functions and methods that can
  [fit on a screen or two of a standard terminal](https://www.kernel.org/doc/Documentation/CodingStyle)
  --- no more than approximately 40 lines.

* unless it makes code less readable, adhere to
  [PEP 8](http://legacy.python.org/dev/peps/pep-0008/) style
  recommendations --- use an appropriate amount of whitespace.

* [code comments should be about *what* is being done, not *how* it is being done](https://www.kernel.org/doc/Documentation/CodingStyle)
  --- that should be self-evident from the code itself.