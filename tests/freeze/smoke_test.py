"""Build a cx_Freeze executable and exercise it against real sample files.

Regression test for https://github.com/deanmalmgren/textract/issues/374,
where freezing with cx_Freeze silently dropped textract's importlib-routed
parser modules and broke the PATH lookups that shell-based parsers (e.g.
.doc via LibreOffice, image OCR via tesseract) depend on.
"""

import shutil
import subprocess
import sys
from pathlib import Path

FREEZE_DIR = Path(__file__).parent
TESTS_DIR = FREEZE_DIR.parent
EXE_NAME = (
    "textract_freeze_smoke.exe" if sys.platform == "win32" else "textract_freeze_smoke"
)

# extension -> sample file, chosen to cover both pure-python parsers
# (txt, docx) and parsers that shell out to external tools (doc via
# LibreOffice, jpg via tesseract)
SAMPLES = {
    "txt": TESTS_DIR / "txt" / "raw_text.txt",
    "docx": TESTS_DIR / "docx" / "raw_text.docx",
    "doc": TESTS_DIR / "doc" / "raw_text.doc",
    "jpg": TESTS_DIR / "jpg" / "raw_text.jpg",
}


def _find_executable(build_root: Path) -> Path:
    for exe_dir in build_root.glob("exe.*"):
        exe = exe_dir / EXE_NAME
        if exe.exists():
            return exe
    msg = f"no built executable named {EXE_NAME!r} found under {build_root}"
    raise FileNotFoundError(msg)


def main() -> None:
    build_root = FREEZE_DIR / "build"
    shutil.rmtree(build_root, ignore_errors=True)
    subprocess.run(
        [sys.executable, str(FREEZE_DIR / "freeze_setup.py"), "build_exe"],
        cwd=FREEZE_DIR,
        check=True,
    )
    exe = _find_executable(build_root)

    failures = []
    for ext, filename in SAMPLES.items():
        result = subprocess.run([str(exe), str(filename)], capture_output=True)
        if result.returncode != 0 or not result.stdout.strip():
            failures.append(ext)
            print(f"FAILED: .{ext} via frozen executable", file=sys.stderr)
            print(result.stderr.decode(errors="replace"), file=sys.stderr)
        else:
            print(f"OK: .{ext}")

    if failures:
        print(
            f"\ncx_Freeze smoke test failed for: {', '.join(failures)}", file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
