from pathlib import Path

from cx_Freeze import Executable, setup

setup(
    name="textract-freeze-smoke-test",
    version="0.1",
    options={
        "build_exe": {
            # textract routes file extensions to parser submodules with
            # importlib at runtime (see textract/parsers/__init__.py), and some
            # dependencies (e.g. chardet) ship deeply nested submodules. Neither
            # is visible to cx_Freeze's static import scan, so they must be
            # listed explicitly to be bundled into the frozen build.
            "packages": ["textract", "chardet"],
        },
    },
    executables=[
        Executable(
            str(Path(__file__).parent / "app.py"),
            target_name="textract_freeze_smoke",
        ),
    ],
)
