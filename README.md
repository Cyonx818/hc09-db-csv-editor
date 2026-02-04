# NFL Head Coach '09 CSV Editor

A Python command-line tool for bulk editing CSV files exported from NFL Head Coach '09 save games. Modify player stats, coach attributes, GM skills, and trainer ratings with an interactive menu-driven interface.

## Features

- **Multi-Type Support:** Edit Players, Coaches, GMs, and Trainers
- **Bulk Operations:** Apply changes to entire teams at once
- **Individual Editing:** Fine-tune specific roster members by name
- **Safe Modifications:** Original files preserved; creates new modified copies
- **Interactive CLI:** Menu-driven interface with clear prompts and validation

### Supported Operations

**Players:**
- Maximize potential stats
- Maximize health and durability
- Inflate current stats (50% toward potential)
- Adjust contracts (7-year league minimum)
- Physical enhancements (height, weight, age)
- Name randomization and renaming

**Coaches:**
- Maximize general coaching potential
- Maximize positional coaching skills (requires cskl.csv)
- Max skill points
- Personality adjustments
- Name randomization and renaming

**GMs:**
- Maximize general GM potential
- Maximize positional GM skills (requires gmsk.csv)
- Max skill points
- Personality adjustments

**Trainers:**
- Maximize trainer potential
- Max skill points
- Personality adjustments

## Installation

**Requirements:**
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Option 1: Install via pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git
cd hc09-db-csv-editor

# Install the package
pip install .

# Run via entry point
hc09-editor [path/to/roster.csv]
```

### Option 2: Install in Development Mode

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git
cd hc09-db-csv-editor

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run via entry point
hc09-editor [path/to/roster.csv]
```

### Option 3: Run Without Installation

```bash
# Clone the repository
git clone https://github.com/Cyonx818/hc09-db-csv-editor.git
cd hc09-db-csv-editor

# Run the __main__.py directly
python src/hc09_db_csv_editor/__main__.py [path/to/roster.csv]

# Or run as module from src directory
cd src
python -m hc09_db_csv_editor [path/to/roster.csv]
```

## Quick Start

1. **Export CSV from NFL Head Coach '09:** Use your save game editor to export roster databases as CSV files

2. **Run the editor:**
   ```bash
   # If installed
   hc09-editor players.csv

   # Or without installation (from project root)
   python src/hc09_db_csv_editor/__main__.py players.csv
   ```
   Or run without arguments and enter the file path when prompted.

3. **Navigate the menu:** Choose operations from numbered menu options

4. **Make changes:** Select players/coaches by name or apply bulk edits to teams

5. **Save:** Confirm to save changes (creates `_modified.csv` file)

6. **Import back:** Use your save game editor to import the modified CSV

## Usage Examples

### Edit a Single Player
```
1. Select option 2: "Select a Player by name"
2. Enter first name: "Tom"
3. Enter last name: "Brady"
4. Choose operation (e.g., "1" to maximize potential)
```

### Bulk Edit a Team
```
1. Select option 3: "Modify all Players on a team"
2. Enter team ID from list (e.g., "22" for Patriots)
3. Choose operation to apply to all players
```

### Randomize Names
```
1. Select option 4: "Randomize Player names"
2. Confirm (affects all players in roster)
```

## Project Structure

```
hc09-db-csv-editor/
├── src/                      # Source code
│   └── hc09_db_csv_editor/   # Main package
│       ├── __init__.py       # Package metadata
│       └── __main__.py       # Main application
├── tests/                    # Test suite
├── docs/                     # Documentation
│   └── user/                 # User guides and reference
├── README.md                 # This file
├── CLAUDE.md                 # Development conventions
└── pyproject.toml            # Project configuration
```

## Companion Files

Some features require companion CSV files in the same directory:

| Main File | Companion | Required For |
|-----------|-----------|--------------|
| Coach roster | `cskl.csv` | Positional coaching skills |
| GM roster | `gmsk.csv` | Positional GM skills |

The tool will auto-detect these files and warn if missing.

## Documentation

- **User Guides:** See `docs/user/getting-started/` for detailed tutorials
- **Reference:** See `docs/user/reference/` for complete CSV field documentation
- **Development:** See `CLAUDE.md` for coding conventions and architecture

## Contributing

Contributions welcome! Please:
1. Read `CLAUDE.md` for development conventions
2. Review existing code patterns before making changes
3. Test changes with actual HC09 CSV exports
4. Update documentation for user-facing changes

## License

Community tool for NFL Head Coach '09 modding. Provided as-is for personal use.

## Disclaimer

This tool is independent of EA Sports and is for personal save game modification only. Use at your own risk. Always backup your save files before editing.

## Support

- **Issues:** Report bugs or request features via GitHub Issues
- **Documentation:** Check `docs/user/` for detailed guides
- **Questions:** Review existing issues or create a new one
