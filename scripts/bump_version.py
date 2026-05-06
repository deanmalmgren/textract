#!/usr/bin/env python3
"""Update the version string in pyproject.toml and textract/__init__.py."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]


def _replace(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text()
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Expected 1 match for {pattern!r} in {path}, found {count}")
    path.write_text(updated)


def bump(version: str) -> None:
    _replace(ROOT / "pyproject.toml", r'^version = "[^"]+"', f'version = "{version}"')
    _replace(
        ROOT / "textract/__init__.py",
        r'^VERSION = "[^"]+"',
        f'VERSION = "{version}"',
    )
    print(f"Bumped to {version}. Run `uv lock`")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <version>", file=sys.stderr)
        sys.exit(1)
    bump(sys.argv[1])
