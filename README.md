# textract-py3

Extract text from any document. No muss. No fuss.

This is a maintained fork of [deanmalmgren/textract](https://github.com/deanmalmgren/textract) originally created to replace `*` dependencies that block usage of modern Python tooling like `asdf`, `uvx`, and current `pip` (see [original issue](https://github.com/deanmalmgren/textract/issues/462)). Over time, this fork has continued to receive updates and improvements.

## Overview

More often than not, valuable information is embedded in Word documents, PowerPoint presentations, PDFs, and other formats—so-called "dark data"—that would be useful for textual analysis and visualization. While several packages exist for extracting content from each format individually, textract provides a single interface for extracting content from any file type without irrelevant markup.

## Usage

textract provides two primary interfaces for text extraction:

**Command line:**

```sh
textract path/to/file.extension
```

**Python package:**

```python
import textract
text = textract.process("path/to/file.extension")
```

## Installation

Install with modern Python tooling:

```sh
# Using uvx
uvx textract-py3 path/to/file.pdf

# Using uv
uv tool install textract-py3

# Using asdf
asdf plugin add textract-py3 https://github.com/amrox/asdf-pyapp.git
asdf install textract-py3 latest

# Using mise
mise use -g pipx:textract-py3

# Using pip
pip install textract-py3
```

For system dependencies and detailed installation instructions, see the [installation documentation](docs/installation.rst).

## Supported File Types

textract supports a growing list of file types. If you don't see your format here, please [open an issue](https://github.com/KyleKing/textract-py3/issues) or [contribute a pull request](docs/contributing.rst).

- `.csv` via python builtins
- `.doc` via [antiword](http://www.winfield.demon.nl/)
- `.docx` via [python-docx2txt](https://github.com/ankushshah89/python-docx2txt)
- `.eml` via python builtins
- `.epub` via [ebooklib](https://github.com/aerkalov/ebooklib)
- `.gif` via [tesseract-ocr](https://code.google.com/p/tesseract-ocr/)
- `.htm`, `.html` via [beautifulsoup4](http://beautiful-soup-4.readthedocs.org/en/latest/)
- `.jpg`, `.jpeg` via [tesseract-ocr](https://code.google.com/p/tesseract-ocr/)
- `.json` via python builtins
- `.mp3` via [sox](http://sox.sourceforge.net/), [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/), and [pocketsphinx](https://github.com/cmusphinx/pocketsphinx/)
- `.msg` via [msg-extractor](https://github.com/mattgwwalker/msg-extractor)
- `.odt` via python builtins
- `.ogg` via [sox](http://sox.sourceforge.net/), [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/), and [pocketsphinx](https://github.com/cmusphinx/pocketsphinx/)
- `.pdf` via [pdftotext](http://poppler.freedesktop.org/) (default) or [pdfminer.six](https://github.com/goulu/pdfminer)
- `.png` via [tesseract-ocr](https://code.google.com/p/tesseract-ocr/)
- `.pptx` via [python-pptx](https://python-pptx.readthedocs.org/en/latest/)
- `.ps` via [ps2ascii](https://www.ghostscript.com/doc/current/Use.htm)
- `.rtf` via [unrtf](http://www.gnu.org/software/unrtf/)
- `.tab`, `.tsv` via python builtins
- `.tif`, `.tiff` via [tesseract-ocr](https://code.google.com/p/tesseract-ocr/)
- `.txt` via python builtins
- `.wav` via [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/) and [pocketsphinx](https://github.com/cmusphinx/pocketsphinx/)
- `.xls`, `.xlsx` via [xlrd](https://pypi.python.org/pypi/xlrd)

## Development

This fork uses `uv` for dependency management and development workflows.

```sh
# # Install system dependencies (macOS)
# brew bundle

# Setup Python environment
uv sync

# Run tests
uv run pytest

# Preview unreleased changelog entries
mise run changelog:preview

# Bump version and release
mise run release:bump -- --increment MINOR  # or PATCH, MAJOR

# Update changelog (semi-automated)
mise run changelog:update
# Or update docs/changelog.rst manually

# Build and publish
uv build && uv publish
```

For contributing guidelines, see the [contributing documentation](docs/contributing.rst).

### Local Testing

Test CI workflows locally using Act (Linux/macOS only) or debug Windows-specific issues using cloud VMs. See the [local testing guide](docs/local-testing.md) for detailed instructions.

GitHub Codespaces (Recommended)
  - Cost: Free (60 hours/month on 2-core)
  - Setup: Zero - just create Windows codespace from repo
  - Best for: Quick debugging of CI failures
  - URL: https://github.com/KyleKing/textract-py3 → Code → Codespaces

## Documentation

Full documentation is available in the `docs/` directory:

- [Command Line Interface](docs/command_line_interface.rst)
- [Python Package API](docs/python_package.rst)
- [Installation Guide](docs/installation.rst)
- [Contributing](docs/contributing.rst)
- [Changelog](docs/changelog.rst)

## Related Projects

textract isn't the first project aiming to provide a simple interface for extracting text from documents. However, it is notable for being written in Python (commonly used in NLP) and being method-agnostic about content extraction. Similar projects include:

- [Apache Tika](http://tika.apache.org/) - Similar aims with impressive format coverage, written in Java
- [textract (node.js)](https://github.com/dbashford/textract) - Similar functionality, written in Node.js
- [pandoc](http://johnmacfarlane.net/pandoc/) - Document conversion tool with plain text output capability, written in Haskell
