# Textract-py3

This is a minimally maintained fork of [deanmalmgren/textract](https://github.com/deanmalmgren/textract) to replace '*' dependencies because they block usage of `asdf`, `uvx` and modern `pip` (open issue: https://github.com/deanmalmgren/textract/issues/462). However, overtime this fork has continued to receive small updates and improvements.

## Usage

Install with `asdf plugin add textract-py3 https://github.com/amrox/asdf-pyapp.git` and `asdf install textract-py3 latest` or with `uvx` (`uv tool install textract-py3`), `mise use -g pipx:textract-py3`, etc.

## Development

This fork has been migrated to `uv`. To run locally and release:

```sh
uv sync
uv run bumpversion minor
uv build && uv publish
```
