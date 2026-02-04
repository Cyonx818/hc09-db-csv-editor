---
audience: user
---

# Installation Guide

> **Purpose:** Get the NFL Head Coach '09 CSV Editor installed and ready to use.
> **Time Required:** 5 minutes
> **Prerequisites:** Python 3.x installed on your system

## System Requirements

### Minimum Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python:** Version 3.6 or higher
- **Disk Space:** <1 MB for the tool itself
- **Memory:** Minimal (standard Python runtime)

### Checking Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

You should see output like `Python 3.x.x`. If not, install Python from [python.org](https://www.python.org/downloads/).

## Installation Steps

### Option 1: Install with pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git

# Navigate to directory
cd hc09-db-csv-editor

# Install the package
pip install .

# Verify installation
hc09-editor --help
```

### Option 2: Development Installation

For contributors or those who want to modify the code:

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git

# Navigate to directory
cd hc09-db-csv-editor

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
hc09-editor --help
```

### Option 3: Run Without Installation

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git

# Navigate to directory
cd hc09-db-csv-editor

# Run as Python module from src directory
cd src
python -m hc09_db_csv_editor --help

# Or run the __main__.py directly
cd ..
python src/hc09_db_csv_editor/__main__.py --help
```

### Option 4: Download ZIP

1. Visit the [GitHub repository](https://github.com/Cyonx818/hc09-db-csv-editor)
2. Click "Code" → "Download ZIP"
3. Extract to your preferred location
4. Open terminal in the extracted directory
5. Follow Option 1 or Option 3 above

## Verifying Installation

### If Installed with pip:

```bash
hc09-editor
```

You should see a prompt: `Enter the path to the input CSV file:`

Type `q` and press Enter to exit.

### If Running Without Installation:

```bash
python -m hc09_db_csv_editor
```

You should see the same prompt.

## No Dependencies Required

This tool uses only Python standard library modules:
- `csv` - CSV file reading/writing
- `os` - File path operations
- `argparse` - Command-line argument parsing
- `random` - Name randomization

No `pip install` required!

## Troubleshooting

### "Python not found" error

**Windows:** Make sure Python is added to PATH during installation. Reinstall Python and check "Add Python to PATH".

**macOS/Linux:** You may need to use `python3` instead of `python`:

```bash
python3 -m hc09_db_csv_editor
```

### "Module not found" error

If you see `ModuleNotFoundError: No module named 'hc09_db_csv_editor'`:

1. **Not installed:** Either install with `pip install .` or run without installation using `python -m hc09_db_csv_editor`
2. **Wrong directory:** If running without installation, ensure you're in the project root directory (not inside `src/`)

### "File not found" error

When running without installation, ensure you're in the project root directory:

```bash
# Check current directory
pwd  # macOS/Linux
cd   # Windows

# List directories (should see src/, docs/, tests/)
ls   # macOS/Linux
dir  # Windows
```

## Next Steps

- **First-time users:** Continue to [Quick Start Guide](quickstart.md)
- **Experienced users:** See [Usage Guide](../guides/usage.md) for detailed operations
- **Advanced users:** Review [CSV Reference](../reference/csv-fields.md) for field documentation

## Uninstallation

Simply delete the `hc09-db-csv-editor` directory. No registry entries or system files are created.
