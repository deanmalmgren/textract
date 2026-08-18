# Built once against the newest supported Python (see requires-python in
# pyproject.toml for the floor). The venv is prebuilt and shipped behind the
# `textract` entrypoint, so the interpreter inside is an implementation
# detail, not something callers select. If that stops being true (someone
# wants to import textract from their own Python code in this image, say),
# turn this into an ARG PYTHON_VERSION and matrix the build in CI.
FROM python:3.14-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /usr/local/bin/
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY pyproject.toml uv.lock README.rst ./
COPY textract ./textract
RUN uv sync --locked --no-dev --no-editable

# Everything below is the whole optional dependency set (LibreOffice,
# tesseract, ghostscript, poppler, sox) -- see the `-full` tag note in
# docs/installation.rst. A lighter, feature-scoped image would start here:
# swap this apt-get list for a subset, or drop it and let the caller add
# only the tools their formats need on top of the venv above.
FROM python:3.14-slim-trixie
RUN apt-get update && apt-get install -y --no-install-recommends \
        dbus-x11 \
        ghostscript \
        libreoffice-writer \
        libsox-fmt-mp3 \
        poppler-utils \
        sox \
        tesseract-ocr \
        unrtf \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
ENTRYPOINT ["textract"]
