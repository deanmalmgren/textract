from __future__ import annotations

from pathlib import Path
import re
from typing import Any
import shutil
import subprocess
import tempfile

import textract


def _normalize_whitespace(content: bytes) -> list[bytes]:
    """Normalize whitespace for comparison.

    Converts all whitespace (tabs, spaces, nbsp, etc.) to single spaces,
    removes blank lines, and normalizes line endings.
    """
    lines = [line for line in content.splitlines() if line.strip()]
    normalized = []
    for line in lines:
        processed = (
            line.replace(b"\t", b" ")
            .replace(b"\r", b" ")
            .replace(b"\xc2\xa0", b" ")
        )
        processed = re.sub(rb" +", b" ", processed).strip()
        if processed:
            normalized.append(processed)
    return normalized


def _files_equal_ignore_blank_lines(file1: str, file2: str) -> bool:
    """Compare two files, ignoring blank lines and normalizing whitespace."""
    content1 = Path(file1).read_bytes()
    content2 = Path(file2).read_bytes()
    lines1 = _normalize_whitespace(content1)
    lines2 = _normalize_whitespace(content2)
    return lines1 == lines2


def _format_diff_message(lines1: list[bytes], lines2: list[bytes], header: str) -> str:
    msg_parts = [f"\n{header}", f"Line counts: {len(lines1)} vs {len(lines2)}"]

    min_lines = min(len(lines1), len(lines2))
    first_diff_idx = next(
        (i for i in range(min_lines) if lines1[i] != lines2[i]), None
    )

    if first_diff_idx is not None:
        msg_parts.extend([
            f"First difference at line {first_diff_idx + 1}:",
            f"  Actual:   {lines1[first_diff_idx]!r}",
            f"  Expected: {lines2[first_diff_idx]!r}",
        ])
    elif len(lines1) != len(lines2):
        msg_parts.append("Files differ in length (all common lines match)")

    msg_parts.append("\nActual output (first 3 lines):")
    msg_parts.extend(f"  {i + 1}: {line!r}" for i, line in enumerate(lines1[:3]))
    msg_parts.append("\nExpected output (first 3 lines):")
    msg_parts.extend(f"  {i + 1}: {line!r}" for i, line in enumerate(lines2[:3]))

    return "\n".join(msg_parts)


def _generate_file_diff_message(file1: str, file2: str) -> str:
    """Generate detailed diff message for file comparison failures."""
    content1 = Path(file1).read_bytes()
    content2 = Path(file2).read_bytes()
    return _format_diff_message(
        _normalize_whitespace(content1),
        _normalize_whitespace(content2),
        f"Files differ: {file1} vs {file2}",
    )


def _generate_bytes_diff_message(actual: bytes, expected: bytes, label: str) -> str:
    """Generate detailed diff message comparing actual bytes against expected bytes."""
    return _format_diff_message(
        _normalize_whitespace(actual),
        _normalize_whitespace(expected),
        f"Python output differs from {label}",
    )


# ---------------------------------------------------------------------------
# Temp file utilities
# ---------------------------------------------------------------------------

def get_temp_filename(extension: str | None = None) -> str:
    stream = tempfile.NamedTemporaryFile(delete=False)
    stream.close()
    filename = stream.name
    if extension is not None:
        filename += "." + extension
        shutil.move(stream.name, filename)
    return filename


def _clean_text(text: bytes) -> bytes:
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if not line.strip():
            continue
        processed = (
            line.replace(b"\t", b" ")
            .replace(b"\r", b"")
            .replace(b"\xc2\xa0", b" ")
            .rstrip()
        )
        if processed:
            cleaned_lines.append(processed)
    return b"\n".join(cleaned_lines)


# ---------------------------------------------------------------------------
# File-path helpers
# ---------------------------------------------------------------------------

def get_extension_directory(extension: str) -> str:
    return str(Path(__file__).resolve().parent / extension)


def _get_filename(extension: str, filename_root: str, default_filename_root: str) -> str:
    root = filename_root or default_filename_root
    path = Path(get_extension_directory(extension)) / f"{root}.{extension}"
    if not path.exists():
        raise FileNotFoundError(
            f'expected filename "{path}" to exist for testing purposes but it doesn\'t'
        )
    return str(path)


def raw_text_filename(extension: str, root: str = "") -> str:
    return _get_filename(extension, root, "raw_text")


def _standardized_text_filename(extension: str, root: str = "") -> str:
    return _get_filename(extension, root, "standardized_text")


def get_expected_filename(filename: str, **kwargs: Any) -> str:
    path = Path(filename)
    basename = path.stem
    if method := kwargs.get("method"):
        basename += f"-m={method}"
    return str(path.parent / f"{basename}.txt")


def _get_standardized_text(extension: str) -> bytes:
    filename = Path(get_extension_directory(extension)) / "standardized_text.txt"
    if filename.exists():
        standardized_text = filename.read_bytes()
    else:
        standardized_text = b"the quick brown fox jumps over the lazy dog"
    return b"".join(standardized_text.split())


# ---------------------------------------------------------------------------
# CLI / Python output helpers
# ---------------------------------------------------------------------------

def _assert_successful_textract(
    filename: str, cleanup: bool = True, **kwargs: Any
) -> str | None:
    temp_filename = get_temp_filename()
    cmd = ["textract"]
    for key, val in kwargs.items():
        cmd.append(f"--{key}={val}")
    cmd.append(filename)

    with Path(temp_filename).open("wb") as output_file:
        result = subprocess.run(
            cmd,
            stdout=output_file,
            stderr=subprocess.PIPE,
            check=False,
        )

    assert result.returncode == 0, (
        f"textract command failed with exit code {result.returncode}: "
        f"{result.stderr.decode('utf-8', errors='ignore')}"
    )

    if cleanup:
        Path(temp_filename).unlink()
        return None
    return temp_filename


def compare_cli_output(
    filename: str, expected_filename: str | None = None, **kwargs: Any
) -> None:
    """Run textract CLI on filename and assert output matches expected_filename.

    Args:
        filename: Path to the input file.
        expected_filename: Path to the .txt reference file. Defaults to
            ``<filename_stem>.txt`` in the same directory, optionally suffixed
            with ``-m=<method>`` when ``method`` is in kwargs.
        **kwargs: Options forwarded to textract (e.g. ``method="pdfminer"``).
    """
    if expected_filename is None:
        expected_filename = get_expected_filename(filename, **kwargs)

    temp_filename = _assert_successful_textract(filename, cleanup=False, **kwargs)
    assert temp_filename is not None
    if not _files_equal_ignore_blank_lines(temp_filename, expected_filename):
        diff_msg = _generate_file_diff_message(temp_filename, expected_filename)
        Path(temp_filename).unlink()
        raise AssertionError(diff_msg)
    Path(temp_filename).unlink()


def compare_python_output(
    filename: str, expected_filename: str | None = None, **kwargs: Any
) -> None:
    """Call textract.process() on filename and assert output matches expected_filename.

    Args:
        filename: Path to the input file.
        expected_filename: Path to the .txt reference file. Defaults to
            ``<filename_stem>.txt`` in the same directory, optionally suffixed
            with ``-m=<method>`` when ``method`` is in kwargs.
        **kwargs: Options forwarded to textract.process() (e.g. ``method="pdfminer"``).
    """
    if expected_filename is None:
        expected_filename = get_expected_filename(filename, **kwargs)

    result = textract.process(filename, **kwargs)
    expected_content = Path(expected_filename).read_bytes()
    cleaned_result = _clean_text(result)
    cleaned_expected = _clean_text(expected_content)
    if cleaned_result != cleaned_expected:
        diff_msg = _generate_bytes_diff_message(cleaned_result, cleaned_expected, expected_filename)
        raise AssertionError(diff_msg)


# ---------------------------------------------------------------------------
# Standard test runners (called by format test modules)
# ---------------------------------------------------------------------------

def run_raw_text_cli(extension: str, filename_root: str = "") -> None:
    compare_cli_output(raw_text_filename(extension, filename_root))


def run_raw_text_python(extension: str, filename_root: str = "") -> None:
    compare_python_output(raw_text_filename(extension, filename_root))


def run_standardized_text_cli(extension: str, filename_root: str = "") -> None:
    filename = _standardized_text_filename(extension, filename_root)
    temp_filename = _assert_successful_textract(filename, cleanup=False)
    assert temp_filename is not None
    try:
        content = Path(temp_filename).read_bytes()
        expected = _get_standardized_text(extension)
        assert b"".join(content.split()) == expected
    finally:
        Path(temp_filename).unlink(missing_ok=True)


def run_standardized_text_python(extension: str, filename_root: str = "") -> None:
    filename = _standardized_text_filename(extension, filename_root)
    result = textract.process(filename)
    expected = _get_standardized_text(extension)
    assert b"".join(result.split()) == expected


def run_filename_spaces(extension: str, filename_root: str = "") -> None:
    raw_filename = raw_text_filename(extension, filename_root)
    temp_filename = get_temp_filename()
    spaced_filename = temp_filename + f" a filename with spaces.{extension}"
    shutil.copyfile(raw_filename, spaced_filename)
    try:
        compare_cli_output(spaced_filename, get_expected_filename(raw_filename))
    finally:
        Path(temp_filename).unlink(missing_ok=True)
        Path(spaced_filename).unlink(missing_ok=True)
