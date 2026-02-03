# Contributing to textract

Maintained fork of [deanmalmgren/textract](https://github.com/deanmalmgren/textract) focused on minimizing dependencies and supporting modern Python.

## Quick Start

```bash
git clone https://github.com/deanmalmgren/textract.git
cd textract
uv sync --group dev
uv run pytest
```

## Development Environment

### Setup

```bash
# Install dependencies
uv sync --group dev

# Install optional dependencies
uv sync --all-extras

# Install system dependencies (macOS)
brew install antiword tesseract ghostscript poppler sox

# Install system dependencies (Ubuntu/Debian)
apt-get install antiword tesseract-ocr ghostscript poppler-utils sox libsox-fmt-mp3
```

### Running Tests

```bash
# Run full test suite
uv run pytest

# Run specific test file
uv run pytest tests/test_core.py

# Run with verbose output
uv run pytest -v

# Skip network tests
SKIP_NETWORK_TESTS=true uv run pytest
```

### Code Quality

```bash
# Type checking
uv run pyright

# Linting and formatting
uv run ruff check
uv run ruff format

# Fix auto-fixable issues
uv run ruff check --fix
```

## Local CI Testing

### Linux/macOS with Act

Act runs GitHub Actions workflows locally using Docker. Windows workflows not supported.

```bash
# Install
brew install act

# List available jobs
./scripts/test-with-act.sh list

# Run Ubuntu tests (fastest)
./scripts/test-with-act.sh

# Run specific matrix combinations
./scripts/test-with-act.sh test-ubuntu-3.9
./scripts/test-with-act.sh test-macos-3.14

# Run with custom options
act -j test --matrix os:ubuntu-latest --matrix python-version:3.9
```

**Limitations:**
- No Windows support
- Docker required
- First run downloads large images (~GB)
- Some system dependencies may need manual setup

**Troubleshooting:**

```bash
# Interactive debugging
act -j test --matrix os:ubuntu-latest --shell

# Clean up containers
docker ps -a | grep act | awk '{print $1}' | xargs docker rm -f

# Remove old images
docker images | grep act | awk '{print $3}' | xargs docker rmi -f
```

### Windows Testing

Act doesn't support Windows. Use cloud VMs for Windows debugging:

| Option | Best For | Cost | Setup |
|--------|----------|------|-------|
| GitHub Codespaces | Quick debugging (<1hr) | Free (60hr/month) | Zero setup |
| Oracle Cloud Free Tier | Extended testing | Free (always) | Moderate setup |
| Azure Free Trial | First-time users | $100-200 credit | Moderate setup |
| Local VM (UTM/Parallels) | Frequent testing | One-time/$99/year | High setup |

**GitHub Codespaces (recommended for quick tests):**

```bash
# Create Windows codespace at https://github.com/deanmalmgren/textract
# Inside codespace:
choco install tesseract ghostscript sox.portable poppler -y
uv sync --all-extras
uv run pytest
```

**Windows setup script (`setup-windows.ps1`):**

```powershell
# Install Chocolatey
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install dependencies
choco install -y tesseract ghostscript sox.portable poppler python --version=3.14 git
pip install uv

# Clone and test
git clone https://github.com/deanmalmgren/textract
cd textract
uv sync --all-extras
$env:SKIP_NETWORK_TESTS="true"
uv run pytest
```

## Releasing

Publishing is automated via GitHub Actions with [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers). No API tokens needed.

### Initial Setup (one-time)

Configure Trusted Publishing on PyPI:

1. Go to https://pypi.org/manage/project/textract/settings/publishing/
2. Add new Trusted Publisher:
   - **PyPI Project Name**: `textract`
   - **Owner**: `KyleKing`
   - **Repository name**: `textract`
   - **Workflow name**: `ci_pipeline.yml`
   - **Environment name**: `pypi`
3. Configure GitHub Environment:
   - Go to repository Settings → Environments
   - Create environment named `pypi`
   - Enable "Required reviewers" for production safety

### Publishing a Release

```bash
# Check current version
uv run cz version --project

# Preview unreleased changes
mise run changelog:preview

# Bump version (PATCH, MINOR, or MAJOR)
mise run release:bump -- --increment MINOR

# For rc/beta releases
uv run cz bump --prerelease rc

# Update changelog (semi-automated)
mise run changelog:update

# Push to trigger automated publishing
git push origin main --tags
```

The `cz bump` command automatically:
- Updates version numbers in `pyproject.toml` and `textract/__init__.py`
- Creates git commit with changes
- Creates git tag (format: `v2.1.2`)

After pushing the tag, GitHub Actions automatically:
- Runs tests across multiple Python versions and operating systems
- Builds package with `uv build`
- Publishes to PyPI using Trusted Publishers
- Generates changelog from commit messages
- Creates GitHub Release with changelog

### Changelog Management

The project maintains a manual changelog in `docs/changelog.rst`. Three options:

**Option 1: Semi-Automated (recommended)**

```bash
# Preview unreleased changes
mise run changelog:preview

# After bumping version, update changelog
mise run changelog:update

# Review and commit
diff docs/changelog.rst.backup docs/changelog.rst
git add docs/changelog.rst
rm docs/changelog.rst.backup
```

Generates new entries from conventional commits and prepends to existing changelog without destroying history.

**Option 2: Manual Updates**

After bumping versions, manually add entries to `docs/changelog.rst` under "latest changes in development for next release".

**Option 3: Full Auto-Generation**

```bash
# Preview auto-generated changelog
uv run cz changelog --dry-run

# Generate complete changelog (overwrites existing)
uv run cz changelog
```

**Warning:** Auto-generation overwrites the existing changelog and changes format. Use with caution.

**Changelog format:** Use conventional commit prefixes (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`) for auto-generated changelogs to categorize commits properly.

## System Dependencies

Some file types require system-level tools:

### macOS

```bash
brew install antiword tesseract ghostscript poppler sox
```

### Ubuntu/Debian

```bash
apt-get install antiword tesseract-ocr ghostscript poppler-utils sox libsox-fmt-mp3 unrtf
```

### Windows

```powershell
choco install antiword tesseract ghostscript sox.portable poppler
```

### File Type Support

- `.doc` requires `antiword`
- `.pdf` requires `pdftotext` (from poppler-utils) or uses built-in `pdfminer`
- `.jpg`, `.png` require `tesseract` for OCR
- `.ps` requires `ghostscript`
- `.rtf` requires `unrtf`
- `.wav` requires `sox` and `SpeechRecognition`

## Project Philosophy

The overarching goal is to make it as easy as possible to extract raw text from any document for natural language processing tasks. In practice:

- Prioritize correct word order over formatting
- Support multiple extraction methods for each file type
- Provide reasonable defaults (tools that produce correct word sequences)
- Remain agnostic about downstream text analysis
- Maintain excellent documentation

## Pull Requests

When submitting PRs:

- Include tests for new functionality
- Update documentation if adding features or changing behavior
- Follow existing code style (enforced by ruff)
- Use conventional commit messages for changelog generation
- Ensure CI passes on all platforms before requesting review
