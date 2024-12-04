# Textract-py3

This is a minimally maintained fork of [deanmalmgren/textract](https://github.com/deanmalmgren/textract) to replace '*' dependencies because they block usage of `asdf`, `uvx` and modern `pip` (open issue: https://github.com/deanmalmgren/textract/issues/461).

## Usage

Install with `asdf plugin add textract-py3 https://github.com/amrox/asdf-pyapp.git` and `asdf install textract-py3 latest` or with `uvx` (`uv tool install textract-py3`), `mise`, etc.

## Development

This fork has been migrated to `poetry` and does not have CI/CD. For local testing and release, use:

```sh
poetry install --sync
poetry run bumpversion minor
poetry publish --build
```
