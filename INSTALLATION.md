# Installation Guide

## Quick Install

The package uses a standard `src/` layout and can be installed directly from GitLab.

### Using pip

```bash
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

### Using uv (recommended)

```bash
uv pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

## How It Works

The package uses modern Python packaging with:
- **src/ layout**: Package code is in `src/etabs_wrapper/`
- **pyproject.toml**: Configured with Hatchling build backend
- **Automatic discovery**: Hatchling automatically finds and packages the `src/etabs_wrapper/` folder

When you run `pip install` or `uv pip install`, the build system:
1. Reads `pyproject.toml` configuration
2. Discovers the package in `src/etabs_wrapper/`
3. Builds a wheel with the correct structure
4. Installs it to your Python environment's `site-packages/`

## Installation Methods

### 1. Direct from GitLab (Recommended for Users)

Install the latest version from the main branch:

```bash
# With pip
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git

# With uv
uv pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

### 2. Install Specific Branch or Tag

Install from a specific branch:

```bash
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git@feature-branch
```

Install from a specific tag/release:

```bash
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git@v0.1.0
```

### 3. Install from requirements.txt

Add to your `requirements.txt`:

```txt
etabs-wrapper @ git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

Then install:

```bash
pip install -r requirements.txt
```

### 4. Install with uv in pyproject.toml

Add to your project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "etabs-wrapper @ git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git",
]
```

Then install:

```bash
uv sync
```

### 5. Development Installation

For contributing or modifying the package:

```bash
# Clone the repository
git clone https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
cd etabs-wrapper

# Install in editable mode with uv (recommended)
uv sync

# Or with pip in editable mode
pip install -e .

# Or with pip including dev dependencies
pip install -e ".[dev]"
```

**Editable mode** (`-e` flag) means:
- Changes to the source code immediately affect the installed package
- No need to reinstall after each change
- Perfect for development

## Package Structure

After installation, the package structure is:

```
site-packages/
└── etabs_wrapper/
    ├── __init__.py
    ├── client.py
    ├── core/
    │   ├── __init__.py
    │   └── connection.py
    ├── results/
    │   ├── __init__.py
    │   └── tables.py
    ├── analysis/
    │   └── __init__.py
    └── model/
        └── __init__.py
```

The `src/` folder is only present in the repository - it's not included in the installed package.

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows (ETABS COM interface is Windows-only)
- **ETABS**: Must be installed on your system
- **Dependencies**: comtypes, pandas, numpy (installed automatically)

## Verifying Installation

After installation, verify it works:

```bash
# Check package is installed
python -c "import etabs_wrapper; print(etabs_wrapper.__version__)"
```

Expected output:
```
0.1.0
```

Or check the package location:

```bash
python -c "import etabs_wrapper; print(etabs_wrapper.__file__)"
```

Expected output (example):
```
C:\Users\YourName\AppData\Local\Programs\Python\Python311\Lib\site-packages\etabs_wrapper\__init__.py
```

## First Time Setup

### 1. COM Type Library Generation

The first time you use the package, `comtypes` needs to generate Python wrappers for the ETABS COM interface. This happens automatically but may take a few seconds.

### 2. Testing the Connection

Create a simple test script (`test_connection.py`):

```python
from etabs_wrapper import ETABSClient, ETABSConnectionError

try:
    client = ETABSClient.from_running_instance()
    print("✓ Connected successfully!")

    ret, filename = client.model.GetModelFilename()
    print(f"✓ Current model: {filename}")

except ETABSConnectionError as e:
    print(f"✗ Connection failed: {e}")
    print("\nPlease ensure:")
    print("  1. ETABS is running")
    print("  2. A model is open")
```

Make sure:
1. ETABS is running
2. A model is open (any model works)
3. Run the script: `python test_connection.py`

## Troubleshooting

### "Could not connect to running ETABS instance"

**Solution**: Make sure ETABS is running and a model file is open.

### "Module 'comtypes.gen.ETABSv1' not found"

**Solution**: This is normal on first run. The module will be generated automatically. If it persists, try:

```python
import comtypes.client
comtypes.client.GetModule('ETABSv1.tlb')  # Force generation
```

### "Failed to create ETABS helper object"

**Solution**: ETABS might not be properly installed or registered. Try:
1. Reinstalling ETABS
2. Running Python as Administrator
3. Checking ETABS version compatibility

### "ModuleNotFoundError: No module named 'etabs_wrapper'"

**Solutions**:

1. Check if package is installed:
   ```bash
   pip list | grep etabs-wrapper
   # or
   uv pip list | grep etabs-wrapper
   ```

2. Reinstall the package:
   ```bash
   pip install --force-reinstall git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
   ```

3. Check you're using the correct Python environment:
   ```bash
   python --version
   which python  # Linux/Mac
   where python  # Windows
   ```

### Package Updates

To update to the latest version:

```bash
# With pip
pip install --upgrade git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git

# With uv
uv pip install --upgrade git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

## Uninstallation

```bash
# With pip
pip uninstall etabs-wrapper

# With uv
uv pip uninstall etabs-wrapper
```

## Development Workflow

For contributors working on the package:

```bash
# Clone and setup
git clone https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
cd etabs-wrapper
uv sync

# Make changes to src/etabs_wrapper/...

# Test locally (changes are immediately available)
python main.py
python examples/basic_usage.py

# Run linter
uv run ruff check src/

# Run tests
uv run pytest tests/

# Commit and push
git add .
git commit -m "Your changes"
git push
```

## Dependencies Management

### Updating Dependencies

```bash
# Add a new dependency
uv add pandas>=2.1.0

# Add a dev dependency
uv add --dev pytest

# Update all dependencies
uv sync --upgrade
```

### Lock File

The `uv.lock` file ensures reproducible installations. Commit this file to the repository.

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [examples/basic_usage.py](examples/basic_usage.py) for detailed examples
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for package structure
- Review the API documentation in the code docstrings

## Support

For issues or questions:
- Open an issue on GitLab: https://gitlab.viktor.ai/jmikec/etabs-wrapper/-/issues
- Check ETABS API documentation for available table names and methods
