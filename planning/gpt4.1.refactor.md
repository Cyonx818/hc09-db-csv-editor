# Refactoring Plan for `hc09-db-csv-editor.py`

## Context
This plan is for an agentic AI coding assistant tasked with refactoring the `hc09-db-csv-editor.py` script to improve maintainability, extensibility, and adherence to Python best practices. The script currently relies on global state, has long and repetitive functions, and lacks modularity, type annotations, and robust error handling. The goal is to reorganize the codebase to make it easier to comprehend, modify, and expand.

---

## Refactoring Objectives
1. **Encapsulate Global State**
2. **Improve Class Design**
3. **Decompose Large Functions**
4. **Centralize and Abstract User Input**
5. **Replace Magic Strings/Numbers with Constants or Enums**
6. **Standardize Error Handling**
7. **Separate File I/O from Business Logic**
8. **Reduce Code Duplication**
9. **Add Type Annotations**
10. **Add Docstrings and Comments**
11. **Organize Constants and Configuration**
12. **Enable Unit Testing**
13. **Refactor Menu and Action Handling**
14. **Validate CSV Structure and Handle Errors**
15. **Handle Unused/Stub Functions Appropriately**
16. **Remove Redundant Pass Statements**
17. **Enforce Consistent Code Formatting**

---

## Step-by-Step Refactoring Plan

### 1. Encapsulate Global State
- Identify all global variables (e.g., `roster_type`, `skill_members`, `changes`).
- Refactor to encapsulate state within classes (e.g., `RosterEditor`).
- Pass state as arguments or instance attributes instead of relying on globals.

### 2. Improve Class Design
- Refactor the `Member` class to use inheritance or composition.
- Create subclasses for each roster type (e.g., `Player`, `Coach`, `GM`, `Trainer`).
- Move type-specific logic (e.g., `get_name`, stat handling) into subclasses.

### 3. Decompose Large Functions
- Identify functions that are long or do too much (e.g., `main_menu`, `modify_member`).
- Break them into smaller, single-responsibility functions.
- Ensure each function has a clear, focused purpose.

### 4. Centralize and Abstract User Input
- Refactor user input handling into a dedicated module or class.
- Abstract input collection to allow for mocking or automation in tests.

### 5. Replace Magic Strings/Numbers with Constants or Enums
- Identify all hardcoded strings and numbers (e.g., stat keys, menu options).
- Define them as constants or enums in a dedicated module or section.
- Replace all occurrences in the codebase with these constants/enums.

### 6. Standardize Error Handling
- Refactor to use exceptions for error cases instead of print statements.
- Handle exceptions at appropriate levels, providing clear error messages.

### 7. Separate File I/O from Business Logic
- Move all file reading/writing logic into dedicated functions or classes.
- Ensure business logic operates on in-memory data structures.
- Only perform I/O at the boundaries of the application.

### 8. Reduce Code Duplication
- Identify duplicated logic (e.g., randomizing names, renaming, modifying members).
- Use polymorphism, higher-order functions, or utility modules to consolidate logic.

### 9. Add Type Annotations
- Add type hints to all function signatures and class attributes.
- Use tools like `mypy` to check type correctness.

### 10. Add Docstrings and Comments
- Add docstrings to all public functions and classes.
- Use comments to explain non-obvious logic or decisions.

### 11. Organize Constants and Configuration
- Group related constants into a config module or class.
- Document the purpose of each constant.

### 12. Enable Unit Testing
- Refactor code to make logic testable (e.g., decouple I/O, avoid globals).
- Add unit tests for core functionality using `unittest` or `pytest`.

### 13. Refactor Menu and Action Handling
- Replace verbose menu logic with a data-driven approach (e.g., mapping menu options to functions).
- Store menu definitions in a list or dictionary for easier modification.

### 14. Validate CSV Structure and Handle Errors
- Add validation for CSV headers and structure.
- Provide clear error messages if the format is unexpected.

### 15. Handle Unused/Stub Functions Appropriately
- For stub functions, either implement them or raise `NotImplementedError`.
- Clearly document any intentionally unimplemented features.

### 16. Remove Redundant Pass Statements
- Remove unnecessary `pass` statements.
- Use `raise NotImplementedError()` where appropriate.

### 17. Enforce Consistent Code Formatting
- Use a linter/formatter (e.g., `black`, `flake8`) to enforce style.
- Fix any inconsistent spacing, indentation, or formatting issues.

---

## Implementation Notes
- Refactor incrementally, running tests after each major change.
- Ensure all existing functionality is preserved unless otherwise specified.
- Document all major refactoring decisions in code comments or commit messages.
- After refactoring, update the README with any changes to usage or structure. 