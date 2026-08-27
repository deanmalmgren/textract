"""Central registry of known cross-platform text-extraction differences.

Full parity across platforms isn't achievable for every format: PDF/PS
extraction shells out to Poppler/Ghostscript builds that differ by OS
package manager (apt/brew/choco), and some codecs are unavailable on
Windows builds of their tooling. Rather than silently marking these xfail
in scattered places, every known instance is recorded here once, and both
the test suite's xfail/skip markers and ``docs/platform_differences.rst``
are derived from this list. ``tests/test_platform_limitations.py`` asserts
the docs page mentions every entry, so the two can't silently drift apart.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformLimitation:
    format: str
    platform: str
    reason: str
    tests: str


PLATFORM_LIMITATIONS: tuple[PlatformLimitation, ...] = (
    PlatformLimitation(
        format="MP3",
        platform="Windows",
        reason="sox.portable on Windows lacks libmad for MP3 decoding",
        tests="tests/test_mp3.py::Mp3TestCase",
    ),
    PlatformLimitation(
        format="PDF",
        platform="Windows",
        reason="PDF content may differ on Windows",
        tests=(
            "tests/test_pdf.py::PdfTestCase, "
            "tests/test_source_input.py::SourceInputTestCase::test_cli_stdin"
        ),
    ),
    PlatformLimitation(
        format="PDF (tesseract OCR)",
        platform="Linux (CI)",
        reason="Tesseract OCR output varies by version; Linux CI has different output",
        tests="tests/test_pdf.py::PdfTestCase::test_method_python/test_method_cli",
    ),
    PlatformLimitation(
        format="PostScript (.ps)",
        platform="Windows",
        reason="PS text layout may differ between gswin64c txtwrite and ps2ascii",
        tests="tests/test_ps.py::PsTestCase",
    ),
)


def reason_for(format: str) -> str:
    """Look up a registered limitation's reason string by its ``format`` label."""
    return next(
        limitation.reason
        for limitation in PLATFORM_LIMITATIONS
        if limitation.format == format
    )
