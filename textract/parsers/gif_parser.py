"""Process GIF image files using tesseract."""

import tempfile
from pathlib import Path

from PIL import Image

from .utils import ShellParser


class Parser(ShellParser):
    """Extract text from GIF files using tesseract-ocr.

    Handles both static and animated GIFs by extracting the first frame
    from animated GIFs before processing with tesseract.
    """

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, D102
        # Open the GIF and check if it's animated
        with Image.open(filename) as img:
            # Check if this is an animated GIF (n_frames > 1)
            is_animated = getattr(img, "is_animated", False)

            if is_animated:
                # Extract first frame to temporary file
                img.seek(0)  # Ensure we're on the first frame
                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False,
                ) as tmp_file:
                    temp_filename = tmp_file.name
                    img.save(temp_filename, format="PNG")
                try:
                    # Process the extracted frame
                    result = self._run_tesseract(temp_filename, **kwargs)
                finally:
                    # Clean up temporary file
                    Path(temp_filename).unlink(missing_ok=True)
                return result
            # For static GIFs, process directly
            return self._run_tesseract(filename, **kwargs)

    def _run_tesseract(self, filename, **kwargs):  # noqa: ANN001, ANN202
        """Run tesseract on a single image file."""
        if "language" in kwargs:
            args = ["tesseract", filename, "stdout", "-l", kwargs["language"]]
        else:
            args = ["tesseract", filename, "stdout"]

        stdout, _ = self.run(args)
        return stdout


__all__ = ["Parser"]
