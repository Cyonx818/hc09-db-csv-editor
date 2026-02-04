# Development Conventions - HC09 CSV Editor

> **Purpose:** Development standards and conventions for the NFL Head Coach '09 CSV Editor project.
> **Last Updated:** 2026-02-04

## Project Overview

This is a Python-based command-line tool for editing CSV files exported from NFL Head Coach '09 save games. It provides bulk attribute editing capabilities for players, coaches, GMs, and trainers.

## Technology Stack

- **Language:** Python 3.x
- **Dependencies:** Standard library only (csv, os, argparse, random)
- **Interface:** Interactive CLI with menu-driven navigation

## Code Organization

### File Structure

```
hc09-db-csv-editor/
├── src/                     # Source code (Python package)
│   └── hc09_db_csv_editor/  # Main package
│       ├── __init__.py      # Package metadata and exports
│       └── __main__.py      # Main application script
├── tests/                   # Test suite
│   ├── __init__.py          # Test package marker
│   ├── fixtures/            # Test data fixtures
│   └── README.md            # Testing documentation
├── docs/                    # Documentation
│   ├── user/                # User-facing documentation
│   ├── ops/                 # Operational documentation
│   └── internal/            # Internal/developmental documentation
├── .claude/                 # Claude Code configuration
│   ├── agents/              # Custom specialized agents
│   ├── commands/            # Project-specific workflow commands
│   └── shared/              # Shared fragments, templates, workflows
├── research/                # Research library for development patterns
├── README.md                # Project overview
├── CLAUDE.md                # Development conventions (this file)
├── pyproject.toml           # Project metadata and build configuration
└── .gitignore               # Git ignore rules
```

### Package Structure

The code follows the **src layout** pattern, a modern Python best practice:

**Benefits:**
- Clean separation of source code from tests and documentation
- Prevents accidental imports of uninstalled code
- Supports proper packaging and distribution
- Scales well as project grows

**Package naming:**
- Directory: `hc09_db_csv_editor` (underscores for Python import compatibility)
- PyPI name: `hc09-db-csv-editor` (hyphens for package name convention)
- Import: `import hc09_db_csv_editor`

### Code Structure Conventions

**Package Structure:**
- `__init__.py`: Package metadata, version, exports
- `__main__.py`: Main application logic (allows `python -m` execution)
- Future modularization: Extract classes/functions into separate modules as needed

**Class Design:**
- `Member` class: Represents a single roster entry (player/coach/GM/trainer)
  - Stores data as dictionary
  - Provides `set_stat()` and `get_name()` methods
  - Type detected via roster type header analysis

**Function Organization:**
- Universal roster functions: Work across all roster types
- Type-specific functions: Prefixed with type (e.g., `modify_player`, `modify_coach`)
- IO/UI functions: Handle file operations and user interaction
- Menu-driven architecture: `main_menu()` → type-specific modify functions → action dictionaries

**Naming Conventions:**
- Package/modules: `snake_case` (e.g., `hc09_db_csv_editor`)
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Global variables: `snake_case` (minimize usage)
- CSV keys: 4-character codes (e.g., `PFNA`, `PLNA`, `TGID`)

**Import Conventions:**
- Standard library imports first
- Third-party imports second (none currently)
- Local package imports last
- Group imports by category with blank lines between

## Coding Standards

### Style Guidelines

- **Line Length:** Prefer <120 characters; hard limit 140 characters
- **Indentation:** 4 spaces (no tabs)
- **String Quotes:** Single quotes preferred for strings; double quotes for user-facing messages
- **Comments:** Explain "why" not "what"; use inline comments sparingly

### Data Handling

**CSV Operations:**
- Always use `encoding='utf-8-sig'` when reading CSV files (handles BOM)
- Use `csv.DictReader` and `csv.DictWriter` for header-based access
- Write modified files with `_modified` suffix to preserve originals
- Handle incrementing suffixes (`_modified_1`, `_modified_2`, etc.)

**Input Validation:**
- Validate team IDs against `TEAM_NAMES` dictionary
- Validate stat keys (must be 4 characters, case-sensitive)
- Provide clear error messages for invalid input
- Allow 'q' or 'quit' at any prompt to cancel operation

**State Management:**
- Use global `changes` flag to track modifications
- Use global `roster_type` to determine current roster type
- Use global `skill_members` for coach/GM skill file data
- Prompt for save confirmation before exiting if changes made

### Function Design Principles

**Single Responsibility:**
- Each function should have one clear purpose
- Separate UI logic from data manipulation logic
- Extract common patterns into reusable functions

**Error Handling:**
- Validate file paths before opening
- Check dictionary key existence before access
- Provide user-friendly error messages
- Continue operation on non-critical errors

**User Experience:**
- Print clear menu options with numbered choices
- Echo user selections back for confirmation
- Provide context in prompts (current values, available options)
- Format output for readability (aligned columns, grouped data)

## Game-Specific Knowledge

### Roster Types

The tool detects roster type by examining the first CSV header:

| Header | Type | Description |
|--------|------|-------------|
| `PSA0` | Player | Player roster database |
| `CFDA` | Coach | Coach roster database |
| `TRAB` | Trainer | Trainer roster database |
| `GMAB` | GM | General Manager roster database |

### Stat Limits

```python
MAXPLAYERSTAT = 99      # Maximum player attribute value
MAXHEALTH = 1000        # Maximum health/durability value
MAXSKILLPOINTS = 131000 # Maximum skill points
MAXCOACHSTAT = 5        # Maximum coach attribute value
MAXGMSTAT = 5           # Maximum GM attribute value (same as coach)
MINPLRN = 75            # Minimum player learning rating
```

### Key Operations

**Player Operations:**
- Maximize potential: Set all potential stats (`*x` keys) to max
- Maximize health: Set injury/durability stats to max
- Inflate current stats: Increase stats by 50% of gap to potential
- Resign for peanuts: Set contract to 7 years at league minimum
- Make physical specimen: Increase height/weight by 10%, set age to 21

**Coach/GM Operations:**
- Max general potential: Set core coaching/GM stats to max
- Max positional potential: Requires companion skill file (cskl.csv/gmsk.csv)
- Read the manual: Max out skill points
- Captain personality: Set personality trait ID to 9

### Companion Files

Some roster types require companion skill files:
- **Coaches:** `cskl.csv` (for positional coaching skills)
- **GMs:** `gmsk.csv` (for positional GM skills)

These files are auto-detected in the same directory as the main CSV.

## Development Workflow

### Running the Application

**Development (without installation):**
```bash
# From project root
python -m hc09_db_csv_editor [path/to/roster.csv]

# Or with explicit path
python src/hc09_db_csv_editor/__main__.py [path/to/roster.csv]
```

**After installation:**
```bash
# Install in development mode
pip install -e .

# Run via entry point
hc09-editor [path/to/roster.csv]

# Or via module
python -m hc09_db_csv_editor [path/to/roster.csv]
```

### Installing for Development

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
hc09-editor --help
```

### Adding New Features

1. **Identify roster type scope:** Does this apply to all types or specific ones?
2. **Define action dictionary:** Add to appropriate `modify_*` function in `__main__.py`
3. **Implement action function:** Follow existing patterns for stat modification
4. **Write tests:** Add test cases in `tests/` directory
5. **Update documentation:** Add to user guides if user-facing
6. **Run tests and linting:** Verify code quality before committing

### Testing Approach

**Automated Testing (Future):**
```bash
# Run test suite
pytest

# With coverage
pytest --cov=hc09_db_csv_editor

# Run linting
ruff check src/
black --check src/
```

**Manual Testing Required:**
- Test with actual HC09 CSV exports
- Verify each roster type (Player, Coach, GM, Trainer)
- Test bulk operations on entire teams
- Verify modified CSV can be re-imported to game
- Check edge cases (Free Agents team ID 33, invalid inputs)

**Key Test Scenarios:**
1. Load each roster type and verify detection
2. Modify individual and bulk records
3. Save changes and verify file integrity
4. Cancel operations and verify no changes saved
5. Test with missing companion files (cskl.csv, gmsk.csv)

## Integration with Claude Code

This project uses extensive Claude Code infrastructure:

- **Agents:** Specialized AI agents in `.claude/agents/` for various development tasks
- **Commands:** Workflow automation commands in `.claude/commands/`
- **Research Library:** Technical patterns and best practices in `research/`

When modifying code or documentation, reference the research library for patterns:
- Python best practices: `research/python-*.md` files
- Documentation standards: `research/llm-documentation-frameworks-patterns.md`
- Testing patterns: `research/pytest-*.md` files

## Future Considerations

**Potential Enhancements:**
- Add support for PERV file (personnel view) to enable GM/Trainer renaming
- Batch processing mode for multiple CSV files
- Configuration file for default values
- Undo/redo functionality
- Export operation history/change log
- Automated test suite with pytest
- CI/CD pipeline for testing and releases

**Architecture Evolution:**
- Extract `Member` class to `src/hc09_db_csv_editor/models.py`
- Extract operations to `src/hc09_db_csv_editor/operations/` (player.py, coach.py, etc.)
- Extract IO functions to `src/hc09_db_csv_editor/io.py`
- Extract UI functions to `src/hc09_db_csv_editor/ui.py`
- Refactor action dictionaries into registry pattern
- Add type hints for Python 3.6+ compatibility
- Consider CSV schema validation with pydantic or dataclasses
- Add proper logging instead of print statements

## Contributing Guidelines

When contributing to this project:

1. **Read documentation first:** Review README.md and user guides in `docs/user/`
2. **Follow conventions:** Adhere to code style and naming patterns
3. **Test thoroughly:** Verify changes with actual game CSV files
4. **Update docs:** Keep user documentation in sync with code changes
5. **Use Claude Code commands:** Leverage `/review-and-fix`, `/troubleshoot-and-remediate` for quality assurance

## License & Attribution

This is a community tool for modding NFL Head Coach '09 save files. The tool itself is independent of EA Sports and is provided as-is for personal use.

---

**For questions or issues, consult:**
- User documentation: `docs/user/`
- Research library: `research/`
- Claude Code help: Run `/help` command
