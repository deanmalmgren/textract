# Pinned to 3.13, not the latest Python: pocketsphinx has no prebuilt wheel
# for 3.14 on Linux yet, and building it from source needs a C toolchain.
FROM python:3.13-slim-trixie AS builder

# Install the base Python dependencies
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /usr/local/bin/
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY pyproject.toml uv.lock README.rst ./
COPY textract ./textract
RUN uv sync --locked --no-dev --no-editable --extra pocketsphinx

# Build the 'full' image; excludes LibreOffice, which most users don't need
# (see docs/installation.rst#converting-legacy-doc-files to add it back)
FROM python:3.13-slim-trixie
RUN apt-get update && apt-get install -y --no-install-recommends \
        ghostscript \
        libportaudio2 \
        libsox-fmt-mp3 \
        poppler-utils \
        sox \
        tesseract-ocr \
        unrtf \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
ENTRYPOINT ["textract"]
CMD ["--help"]
