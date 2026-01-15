# Local CI Testing Guide

Guide for testing GitHub Actions workflows locally and debugging cross-platform issues.

## Act: Local Linux/macOS Testing

Act allows you to run GitHub Actions workflows locally using Docker containers. **Note: Windows workflows are not supported.**

### Installation

```bash
# macOS
brew install act

# Or using Go
go install github.com/nektos/act@latest

# Verify installation
act --version
```

### Quick Start

```bash
# List all available jobs
./scripts/test-with-act.sh list

# Run Ubuntu tests (fastest, default)
./scripts/test-with-act.sh

# Run specific matrix combinations
./scripts/test-with-act.sh test-ubuntu-3.9
./scripts/test-with-act.sh test-ubuntu-3.14
./scripts/test-with-act.sh test-macos-3.9
./scripts/test-with-act.sh test-macos-3.14

# Run Act directly with custom options
act -j test --matrix os:ubuntu-latest --matrix python-version:3.9
```

### Configuration

The `.actrc` file configures Act behavior:

- Uses `catthehacker/ubuntu:act-latest` for Ubuntu (includes common tools)
- Uses `ghcr.io/catthehacker/macos:latest` for macOS testing
- Enables container reuse for faster iterations
- Verbose output for debugging

### Limitations

1. **No Windows Support**: Act cannot run Windows workflows locally
2. **Docker Required**: All jobs run in containers
3. **macOS Testing Limited**: macOS containers have platform differences
4. **System Dependencies**: Some tools (tesseract, ghostscript, etc.) may need manual setup in containers
5. **Performance**: First run downloads large images (~GB), subsequent runs are faster with `--reuse`

### Troubleshooting

**Missing system dependencies:**
The custom action at `.github/actions/setup/action.yml` installs system dependencies. If tests fail, you may need to debug the container:

```bash
# Run interactively
act -j test --matrix os:ubuntu-latest --shell

# Inside container, manually install dependencies
apt-get update
apt-get install -y antiword tesseract-ocr sox libsox-fmt-mp3 ghostscript unrtf poppler-utils
```

**Container issues:**
```bash
# Clean up containers
docker ps -a | grep act | awk '{print $1}' | xargs docker rm -f

# Remove old images
docker images | grep act | awk '{print $3}' | xargs docker rmi -f
```

## Windows Testing Options

Since Act doesn't support Windows, here are cloud options for Windows testing:

### Option 1: GitHub Codespaces (Recommended for Quick Tests)

**Best for**: Short debugging sessions (<1 hour), official GitHub integration

**Pros:**
- Pre-configured with GitHub Actions environment
- 60 hours/month free (2-core) or 30 hours/month (4-core) on personal accounts
- Zero setup required
- Same environment as CI

**Cons:**
- Pay after free tier
- Requires internet connection
- Monthly limits

**Usage:**
```bash
# Create a Windows codespace
# Go to: https://github.com/KyleKing/textract-py3
# Click: Code -> Codespaces -> Create codespace on main
# Select: Windows machine type

# Inside codespace
choco install tesseract ghostscript sox.portable poppler -y
uv sync --all-extras
uv run pytest
```

**Cost**: Free tier: 60 hours/month (2-core). Paid: $0.18/hour (2-core), $0.36/hour (4-core)

### Option 2: Oracle Cloud Free Tier (Best for Extended Testing)

**Best for**: Longer debugging sessions, cost-conscious users

**Pros:**
- Always free tier includes Windows VMs
- 1/8 OCPU + 1GB RAM (sufficient for testing)
- No time limits
- No credit card required for free tier

**Cons:**
- Setup complexity (networking, security groups)
- Less integrated with GitHub ecosystem
- May have regional availability issues

**Setup:**
1. Create Oracle Cloud account: https://www.oracle.com/cloud/free/
2. Create Windows VM instance (Always Free eligible)
3. Configure security groups to allow RDP
4. Install dependencies:
   ```powershell
   choco install tesseract ghostscript sox.portable poppler -y
   choco install python --version=3.14
   choco install git
   git clone https://github.com/KyleKing/textract-py3
   cd textract-py3
   pip install uv
   uv sync --all-extras
   uv run pytest
   ```

**Cost**: Free (within always-free tier limits)

### Option 3: Azure for Students / Free Trial

**Best for**: Students or first-time Azure users

**Pros:**
- $100 free credit (students) or $200 (free trial)
- Professional-grade infrastructure
- Good Windows VM performance
- Integrates with Visual Studio

**Cons:**
- Credit card required
- Credits expire (12 months)
- Charges apply after credits exhausted

**Setup:**
1. Sign up: https://azure.microsoft.com/free/students/ (students) or https://azure.microsoft.com/free/ (free trial)
2. Create Windows VM (B1s: 1 vCPU, 1GB RAM ~$0.01/hour)
3. Connect via RDP
4. Install dependencies (same as Oracle Cloud)

**Cost**: Free with credits. After: ~$0.01-0.05/hour for small VMs

### Option 4: Local VM (UTM/Parallels) - One-Time Cost

**Best for**: Frequent Windows testing, offline work

**UTM (Free, M1/M2 Macs):**
```bash
brew install --cask utm
# Download Windows 11 ARM64 ISO from Microsoft
# Create new VM in UTM with downloaded ISO
# Install Windows, then install dependencies
```

**Parallels Desktop ($99/year):**
- Best performance on macOS
- Seamless integration
- Annual subscription

**Pros:**
- Full control
- No ongoing costs (UTM) or predictable costs (Parallels)
- Works offline
- Fast iteration

**Cons:**
- Large disk space (~20GB minimum)
- Requires Windows license
- System resources

### Recommendation Matrix

| Use Case | Duration | Recommendation | Monthly Cost |
|----------|----------|----------------|--------------|
| Quick debug (<1hr) | One-time | GitHub Codespaces | Free |
| Regular testing (weekly) | <5hr/month | GitHub Codespaces | Free |
| Frequent testing | >10hr/month | Oracle Cloud Free | Free |
| Daily development | Any | Local VM (UTM) | One-time HW |
| Professional | Any | Parallels + Azure | ~$100/year |

### Quick Command Reference

**Setup script for Windows:**

Save as `setup-windows.ps1`:
```powershell
# Install Chocolatey if not present
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install dependencies
choco install -y `
    tesseract `
    ghostscript `
    sox.portable `
    poppler `
    python --version=3.14 `
    git

# Install uv
pip install uv

# Clone and test
git clone https://github.com/KyleKing/textract-py3
cd textract-py3
uv sync --all-extras
$env:SKIP_NETWORK_TESTS="true"
uv run pytest
```

## Cross-Platform Testing Strategy

1. **Develop on macOS**: Primary development environment
2. **Test Linux with Act**: Fast feedback loop for Linux compatibility
3. **Test Windows in cloud**: Use Codespaces for quick checks, Oracle Cloud for extended debugging
4. **Fix cross-platform issues**: Focus on path handling, line endings, shell commands

## Common Cross-Platform Issues

### Issue 1: Path Separators

Windows uses backslashes (`\`), Unix uses forward slashes (`/`).

**Solution**: Use `pathlib.Path` (already done in codebase):
```python
# Good (current code)
path = pathlib.Path(directory) / filename

# Bad
path = directory + "/" + filename
```

### Issue 2: Line Endings

Windows uses CRLF (`\r\n`), Unix uses LF (`\n`).

**Solution**: Already handled in `tests/base.py:23`:
```python
lines1 = [line.rstrip(b"\r") for line in content1.splitlines() if line.strip()]
```

### Issue 3: Shell Command Quoting

Different quoting rules on Windows vs Unix.

**Solution**: Already handled in `tests/base.py:12-16`:
```python
def _quote_path(path: str) -> str:
    if sys.platform == "win32":
        return f'"{path}"'
    return f"'{path}'"
```

### Issue 4: External Tool Behavior

Tools like tesseract, ghostscript, poppler may produce slightly different output on different platforms.

**Solution**: Normalize and compare output, allowing for minor differences:
- Strip whitespace
- Ignore blank lines
- Use fuzzy matching for OCR results

### Issue 5: Tool Installation Paths

Windows tools install to different locations (e.g., `Program Files`).

**Potential improvement**: Use `shutil.which()` to find tools dynamically instead of assuming PATH.

## Next Steps

1. Install Act: `brew install act`
2. Run Linux tests locally: `./scripts/test-with-act.sh`
3. For Windows failures, choose cloud option based on table above
4. Document specific Windows failures for future reference
