.PHONY: sync lint test check fix docs docs-serve clean

sync:
	uv sync --all-extras
	@if [ "$$(uname)" = "Darwin" ]; then \
		find .venv -name "_pocketsphinx.cpython-*-darwin.so" -exec codesign -s - -f {} \; 2>/dev/null || true; \
	fi

lint:
	uv run ruff check
	uv run pyright

test:
	uv run pytest

check:
	$(MAKE) lint
	$(MAKE) test

fix:
	uv run ruff format
	uv run ruff check

docs:
	$(MAKE) -C docs html

docs-serve: docs
	@echo "Documentation built at docs/build/html/index.html"
	@if command -v python3 >/dev/null 2>&1; then \
		echo "Serving on http://localhost:8000 (Ctrl+C to stop)"; \
		cd docs/build/html && python3 -m http.server 8000; \
	else \
		echo "python3 not found. Open docs/build/html/index.html manually."; \
	fi

clean:
	rm -rf .venv
	rm -rf docs/build
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true
