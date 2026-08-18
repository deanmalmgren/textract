FROM python:3.14-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /usr/local/bin/
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY pyproject.toml uv.lock README.rst ./
COPY textract ./textract
RUN uv sync --locked --no-dev --no-editable

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
