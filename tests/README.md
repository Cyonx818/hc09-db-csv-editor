# Tests

This directory contains the test suite for the hc09_db_csv_editor package.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hc09_db_csv_editor

# Run specific test file
pytest tests/test_member.py
```

## Test Structure

```
tests/
├── __init__.py           # Test package marker
├── test_member.py        # Tests for Member class
├── test_io.py            # Tests for file I/O operations
├── test_operations.py    # Tests for player/coach operations
└── fixtures/             # Test data fixtures
    └── sample_csvs/      # Sample CSV files for testing
```

## Writing Tests

Follow these conventions:
- Test files named `test_*.py`
- Test functions named `test_*`
- Use pytest fixtures for common setup
- Mock file I/O operations to avoid external dependencies
- Test edge cases and error conditions

## Test Coverage Goals

Target minimum 80% code coverage for:
- Member class operations
- CSV reading/writing
- Stat modification functions
- Input validation
- Error handling

## Future Test Implementation

Tests not yet implemented. Priority areas:
1. Member class initialization and stat setting
2. CSV detection and parsing
3. Player operation functions (max_potential, max_health, etc.)
4. Coach/GM/Trainer operations
5. Name randomization
6. Contract modifications
7. Error handling and edge cases
