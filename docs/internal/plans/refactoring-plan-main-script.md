# Refactoring Plan: __main__.py Module Decomposition

> **Purpose:** Comprehensive plan to refactor the monolithic __main__.py (833 lines) into a modular, maintainable architecture.
> **Created:** 2026-02-04
> **Status:** Planning Phase

---

## Executive Summary

The current __main__.py script mixes UI, business logic, data models, and I/O operations in a single 833-line file with global state management. This refactoring plan proposes a clean separation into specialized modules following the Strategy Pattern for roster type operations, eliminating global variables through dependency injection, and establishing a clear architectural foundation for future extensibility.

**Key Metrics:**
- Current: 1 file, 833 lines, 3 global variables, 60+ functions
- Proposed: 9 modules, ~100 lines per module, 0 global variables
- Architecture: Strategy Pattern with dependency injection
- Breaking changes: None (internal refactor only)

---

## Part 1: Current Architecture Analysis

### 1.1 Identified Issues

| Issue | Severity | Impact | Line References |
|:------|:---------|:-------|:----------------|
| **Global state management** | Critical | Thread safety, testability, state coupling | 102-104, 109, 149-151, 359-361, 384-386, 579, 695, 733, 773, 822 |
| **Monolithic structure** | High | Maintainability, comprehension, code navigation | Entire file |
| **Mixed concerns** | High | Single Responsibility Principle violations | UI (146-219), I/O (221-258), business logic (446-640) |
| **Code duplication** | Medium | DRY violations across roster types | modify_player (565-575) vs modify_coach (719-729) vs modify_gm (785-793) |
| **Limited extensibility** | Medium | Adding new roster types requires scattered changes | 280-290, 350-355, 406-421 |
| **Tight coupling** | Medium | Member class depends on global roster_type | 109, 121-125 |
| **No type hints** | Low | IDE support, documentation, type safety | All function signatures |
| **Print-based output** | Low | No logging abstraction, hard to test | 100+ occurrences |

### 1.2 Global Variables Detailed Analysis

```python
# Line 102-104: Global state variables
skill_members = None      # Used in: 150, 154, 359, 384, 695, 773
changes = False           # Used in: 103, 151, 215, 360, 375, 385, 398, 579, 733
roster_type = ''          # Used in: 104, 109, 121-122, 149, 152, 156, 158-161, 194, 196, 202, 204, 362, 385, 390, 415, 822, 826
```

**Problems:**
1. **Thread safety**: Not safe for concurrent operations
2. **Testability**: Difficult to isolate tests, requires global state reset
3. **State coupling**: Functions implicitly depend on global state
4. **Hidden dependencies**: Not clear from function signatures what state is needed

### 1.3 Function Categorization

| Category | Functions | Current Organization | Issues |
|:---------|:----------|:--------------------|:--------|
| **I/O Operations** | get_input_file, read_members_from_csv, write_members_to_csv, save_changes_confirmation | Lines 130-258 | Mixed with UI functions |
| **UI/Menu** | main_menu, print_team_names, list_roster_by_team, find_member_by_team | Lines 146-442 | Coupled to global state |
| **Player Operations** | max_potential, max_health, inflate_current_stats, resign_for_peanuts, make_physical_specimen, rename_player, randomize_player_names | Lines 446-640 | Duplicate patterns |
| **Coach Operations** | max_general_coaching_potential, max_positional_coaching_potential, rename_coach, randomize_coach_names | Lines 642-763 | Duplicate patterns |
| **GM Operations** | max_general_gm_potential, max_positional_gm_potential | Lines 765-797 | Duplicate patterns |
| **Trainer Operations** | max_trainer_potential | Lines 799-817 | Duplicate patterns |
| **Universal Operations** | captain_personality, change_key_value, read_the_manual | Lines 261-278, 424-426 | Should be abstracted |
| **Infrastructure** | detect_roster_type, find_member_index, find_skill_file, modify_member, modify_bulk_members | Lines 280-422 | Should be framework layer |

### 1.4 Code Duplication Patterns

**Pattern 1: Action Dictionary Structure** (identical across types)
```python
# modify_player (565-575), modify_coach (719-729), modify_gm (785-793)
actions = {
    "1": ("Description", function_reference),
    "2": ("Description", function_reference),
    # ...
}
modify_member(actions, member)
```

**Pattern 2: Roster Listing** (similar across types)
```python
# list_players_by_team (461-513), list_coaches_by_team (643-685)
# - Position abbreviation dictionary
# - Team selection logic
# - Filtering by team ID
# - Formatted display output
```

**Pattern 3: Name Randomization** (identical logic)
```python
# randomize_player_names (578-601), randomize_coach_names (732-755)
# - Collect distinct first/last names into sets
# - Convert to lists
# - Randomly reassign to all members
```

**Pattern 4: Max Potential Functions** (similar structure)
```python
# max_potential (530-538), max_general_coaching_potential (688-691), max_general_gm_potential (766-769)
# - Define stat keys list
# - Iterate and set to max constant
```

---

## Part 2: Proposed Architecture

### 2.1 Module Structure

```
src/hc09_db_csv_editor/
├── __init__.py              # Package metadata, version, public API exports
├── __main__.py              # Entry point (minimal, delegates to cli.py)
├── models.py                # Data models (Member, RosterContext)
├── constants.py             # All constants (TEAM_NAMES, stat limits, stat mappings)
├── io_handler.py            # File I/O operations (CSV read/write, skill file discovery)
├── ui.py                    # User interface (menus, prompts, display formatting)
├── roster_strategy.py       # Abstract base class for roster type strategies
├── operations/              # Roster-specific operation modules
│   ├── __init__.py          # Operations package (exports all strategies)
│   ├── player.py            # PlayerStrategy implementation
│   ├── coach.py             # CoachStrategy implementation
│   ├── gm.py                # GMStrategy implementation
│   └── trainer.py           # TrainerStrategy implementation
└── cli.py                   # CLI orchestration (main application flow)
```

**Module Responsibilities:**

| Module | Responsibility | Lines (est.) | Dependencies |
|:-------|:--------------|:-------------|:-------------|
| `__init__.py` | Package metadata, version, exports | 15 | None |
| `__main__.py` | Entry point, delegates to cli.main() | 10 | cli |
| `models.py` | Member, RosterContext classes | 80 | constants |
| `constants.py` | Constants, enums, stat mappings | 120 | None |
| `io_handler.py` | CSV I/O, file operations | 100 | models, constants |
| `ui.py` | Menus, prompts, formatting | 150 | constants, models |
| `roster_strategy.py` | Abstract strategy base class | 60 | models |
| `operations/player.py` | Player operations strategy | 180 | roster_strategy, models, constants |
| `operations/coach.py` | Coach operations strategy | 160 | roster_strategy, models, constants |
| `operations/gm.py` | GM operations strategy | 100 | roster_strategy, models, constants |
| `operations/trainer.py` | Trainer operations strategy | 80 | roster_strategy, models, constants |
| `cli.py` | Application orchestration | 120 | All modules |

### 2.2 Design Patterns Applied

#### Strategy Pattern for Roster Type Operations

**Problem:** Different roster types (Player, Coach, GM, Trainer) require different operations but share common infrastructure.

**Solution:** Define a common interface via abstract base class, implement concrete strategies for each roster type.

```python
# roster_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Optional

class RosterStrategy(ABC):
    """Abstract base class for roster type-specific operations."""

    @abstractmethod
    def get_roster_type_name(self) -> str:
        """Return the roster type name (e.g., 'Player', 'Coach')."""
        pass

    @abstractmethod
    def get_individual_actions(self) -> Dict[str, tuple[str, Callable]]:
        """Return action dictionary for individual member operations."""
        pass

    @abstractmethod
    def get_bulk_actions(self) -> Dict[str, tuple[str, Callable]]:
        """Return action dictionary for bulk team operations."""
        pass

    @abstractmethod
    def supports_name_search(self) -> bool:
        """Whether this roster type supports searching by name."""
        pass

    @abstractmethod
    def supports_bulk_operations(self) -> bool:
        """Whether this roster type supports bulk team operations."""
        pass

    @abstractmethod
    def get_name_keys(self) -> Optional[tuple[str, str]]:
        """Return (first_name_key, last_name_key) or None."""
        pass

    @abstractmethod
    def list_by_team(self, members: List, team_id: str, ui) -> None:
        """Display roster listing for a team."""
        pass

    @abstractmethod
    def get_skill_file_name(self) -> Optional[str]:
        """Return companion skill file name (e.g., 'cskl.csv') or None."""
        pass
```

**Benefits:**
1. Easy to add new roster types (just implement the interface)
2. Type-specific logic encapsulated in strategy classes
3. Common operations abstracted in base class
4. No global state needed (context passed to strategies)

#### Dependency Injection for State Management

**Problem:** Global variables create tight coupling and hinder testability.

**Solution:** Create a context object that holds application state, pass it explicitly.

```python
# models.py
from typing import List, Optional

class RosterContext:
    """Container for application state (replaces global variables)."""

    def __init__(self,
                 roster_type: str,
                 members: List['Member'],
                 headers: List[str],
                 file_path: str,
                 skill_members: Optional[List['Member']] = None,
                 skill_headers: Optional[List[str]] = None,
                 skill_file_path: Optional[str] = None):
        self.roster_type = roster_type
        self.members = members
        self.headers = headers
        self.file_path = file_path
        self.skill_members = skill_members
        self.skill_headers = skill_headers
        self.skill_file_path = skill_file_path
        self.changes_made = False  # Replaces global 'changes' flag

    def mark_changed(self) -> None:
        """Mark that changes have been made to the roster."""
        self.changes_made = True
```

**Benefits:**
1. Explicit dependencies (visible in function signatures)
2. Thread-safe (each context is independent)
3. Testable (easy to create test contexts)
4. No hidden state coupling

#### Registry Pattern for Strategy Selection

**Problem:** Need to map roster type headers to strategy implementations.

**Solution:** Strategy registry with automatic detection.

```python
# operations/__init__.py
from typing import Dict, Type
from ..roster_strategy import RosterStrategy
from .player import PlayerStrategy
from .coach import CoachStrategy
from .gm import GMStrategy
from .trainer import TrainerStrategy

class StrategyRegistry:
    """Registry for roster type strategies."""

    def __init__(self):
        self._strategies: Dict[str, RosterStrategy] = {
            'PSA0': PlayerStrategy(),    # Player roster header
            'CFDA': CoachStrategy(),      # Coach roster header
            'GMAB': GMStrategy(),         # GM roster header
            'TRAB': TrainerStrategy(),    # Trainer roster header
        }

    def get_strategy(self, header: str) -> RosterStrategy:
        """Get strategy for given CSV header."""
        if header not in self._strategies:
            raise ValueError(f"Unknown roster type header: {header}")
        return self._strategies[header]

    def get_roster_type_name(self, header: str) -> str:
        """Get roster type name from header."""
        return self.get_strategy(header).get_roster_type_name()

# Global registry instance
STRATEGY_REGISTRY = StrategyRegistry()
```

**Benefits:**
1. Single source of truth for roster type detection
2. Easy to register new roster types
3. Decouples header detection from strategy logic

### 2.3 Detailed Module Designs

#### models.py

```python
"""Data models for roster members and application context."""

from typing import Dict, List, Optional

class Member:
    """Represents a single roster entry (player/coach/GM/trainer)."""

    def __init__(self, data: Dict[str, str]):
        self.data = data

    def set_stat(self, stat_key: str, value) -> None:
        """Set a stat value (validates key existence)."""
        if stat_key in self.data:
            self.data[stat_key] = str(value)
        else:
            raise KeyError(f"Stat {stat_key} does not exist in member data")

    def get_stat(self, stat_key: str, default=None):
        """Get a stat value with optional default."""
        return self.data.get(stat_key, default)

    def get_name(self, first_name_key: str, last_name_key: str) -> str:
        """Get formatted name from specified keys."""
        first = self.data.get(first_name_key, '')
        last = self.data.get(last_name_key, '')
        return f"{first} {last}".strip()


class RosterContext:
    """Container for application state."""

    def __init__(self,
                 roster_type: str,
                 members: List[Member],
                 headers: List[str],
                 file_path: str,
                 skill_members: Optional[List[Member]] = None,
                 skill_headers: Optional[List[str]] = None,
                 skill_file_path: Optional[str] = None):
        self.roster_type = roster_type
        self.members = members
        self.headers = headers
        self.file_path = file_path
        self.skill_members = skill_members
        self.skill_headers = skill_headers
        self.skill_file_path = skill_file_path
        self.changes_made = False

    def mark_changed(self) -> None:
        """Mark that changes have been made."""
        self.changes_made = True

    def get_members_by_team(self, team_id: str) -> List[Member]:
        """Filter members by team ID."""
        if team_id == "33":  # Free Agents
            return [m for m in self.members if m.data['TGID'] not in map(str, range(1, 33))]
        return [m for m in self.members if m.data.get('TGID') == team_id]
```

**Eliminates:**
- Global `roster_type` variable
- Global `changes` flag
- Global `skill_members` variable
- Member class dependency on global state (line 109)

#### constants.py

```python
"""Constants and configuration for the HC09 CSV Editor."""

from typing import Dict

# Stat Limits
MAXPLAYERSTAT = 99
MAXHEALTH = 1000
MAXSKILLPOINTS = 131000
MAXCOACHSTAT = 5
MAXGMSTAT = 5
MINPLRN = 75

# CSV Field Keys
PLAYER_FIRST_NAME_CODE = 'PFNA'
PLAYER_LAST_NAME_CODE = 'PLNA'
COACH_FIRST_NAME_CODE = 'CFNM'
COACH_LAST_NAME_CODE = 'CLNM'
TEAM_ID_KEY = 'TGID'
PERSONNEL_ID_KEY = 'PNid'

# Roster Type Headers
PLAYER_HEADER = 'PSA0'
COACH_HEADER = 'CFDA'
TRAINER_HEADER = 'TRAB'
GM_HEADER = 'GMAB'

# Team Names (unchanged)
TEAM_NAMES: Dict[str, str] = { ... }

# Player Stats Mapping (unchanged)
PLAYER_STATS: Dict[str, str] = { ... }

# Position Abbreviations
PLAYER_POSITIONS: Dict[str, str] = { ... }
COACH_POSITIONS: Dict[str, str] = { ... }
```

**Eliminates:**
- Constants scattered in __main__.py (lines 8-98)
- Magic strings throughout code

#### io_handler.py

```python
"""File I/O operations for CSV roster files."""

import csv
import os
from typing import List, Tuple, Optional
from .models import Member
from .constants import TEAM_ID_KEY

class IOHandler:
    """Handles CSV file reading and writing operations."""

    @staticmethod
    def read_csv(file_path: str) -> Tuple[List[str], List[Member]]:
        """Read CSV file and return headers and members."""
        headers = []
        members = []
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            headers = list(reader.fieldnames)
            for row in reader:
                members.append(Member(row))
        return headers, members

    @staticmethod
    def write_csv(members: List[Member], headers: List[str], file_path: str) -> str:
        """Write members to CSV file with _modified suffix."""
        base, ext = os.path.splitext(file_path)
        output_file = base + "_modified" + ext
        count = 1
        while os.path.exists(output_file):
            output_file = f"{base}_modified_{count}{ext}"
            count += 1

        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for member in members:
                writer.writerow(member.data)

        return output_file

    @staticmethod
    def find_skill_file(roster_file_path: str, skill_file_name: str) -> Optional[str]:
        """Find companion skill file in same directory as roster file."""
        directory = os.path.dirname(roster_file_path)
        for filename in os.listdir(directory):
            if filename.lower() == skill_file_name.lower():
                return os.path.join(directory, filename)
        return None

    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Check if file path exists and is a file."""
        return os.path.isfile(file_path)
```

**Eliminates:**
- I/O functions scattered in __main__.py (lines 130-258)
- File path handling logic duplication

#### ui.py

```python
"""User interface functions for interactive CLI."""

import argparse
import os
from typing import List, Optional, Callable, Dict
from .models import Member
from .constants import TEAM_NAMES

class UI:
    """User interface handler for the application."""

    @staticmethod
    def get_input_file_path() -> str:
        """Get input file path from arguments or user prompt."""
        parser = argparse.ArgumentParser(description="Process roster CSV file.")
        parser.add_argument('input_file', nargs='?', help="Path to the input CSV file.")
        args = parser.parse_args()

        if args.input_file and os.path.isfile(args.input_file):
            return args.input_file

        while True:
            file_path = input("Enter the path to the input CSV file: ").strip()
            if os.path.isfile(file_path):
                return file_path
            print("File not found. Please try again.")

    @staticmethod
    def print_team_names() -> None:
        """Display formatted team ID list."""
        print("\nTeam ID List:")
        columns = 4
        col_width = 25
        teams_list = list(TEAM_NAMES.items())
        line = ""
        for i, (team_id, team_name) in enumerate(teams_list):
            formatted_id = f"{int(team_id):02d}"
            line += f"{formatted_id}: {team_name:<{col_width}}"
            if (i + 1) % columns == 0:
                print(line)
                line = ""
        if line:
            print(line)

    @staticmethod
    def prompt_team_id() -> str:
        """Prompt user for team ID selection."""
        UI.print_team_names()
        while True:
            team_id = input("\nEnter team ID (1-33, or 'q' to quit): ").strip()
            if team_id.lower() in ['q', 'quit']:
                return ''
            if team_id in TEAM_NAMES or team_id == '33':
                return team_id
            print(f"Invalid team ID: {team_id}. Please try again.")

    @staticmethod
    def prompt_name(roster_type: str) -> Optional[Tuple[str, str]]:
        """Prompt user for first and last name."""
        first_name = input(f"Enter {roster_type}'s first name (or 'q' to quit): ").strip()
        if first_name.lower() in ['q', 'quit']:
            return None
        last_name = input(f"Enter {roster_type}'s last name (or 'q' to quit): ").strip()
        if last_name.lower() in ['q', 'quit']:
            return None
        return (first_name, last_name)

    @staticmethod
    def display_action_menu(actions: Dict[str, Tuple[str, Callable]], context_label: str) -> Optional[str]:
        """Display action menu and get user choice."""
        print("\nChoose an action to perform:")
        for key, (description, _) in actions.items():
            print(f"{key}. {description}")
        print(f"q. Quit to {context_label}")

        choice = input("\nEnter your choice: ").strip().lower()
        return choice if choice not in ['q', 'quit'] else None

    @staticmethod
    def confirm_save(file_path: str) -> bool:
        """Prompt user to confirm save operation."""
        while True:
            response = input(f"Do you want to save changes to {file_path}? (yes/no): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Invalid input. Please enter 'yes' or 'no'.")

    @staticmethod
    def prompt_key_value_change(member: Member) -> None:
        """Prompt user to change a specific key value."""
        while True:
            key = input("Enter key name to change (4-character, case-sensitive, or 'q' to quit): ").strip()
            if key.lower() in ['q', 'quit']:
                return
            if len(key) != 4:
                print("Invalid key name. It must be a 4-character string.")
                continue
            if key in member.data:
                print(f"Current value for {key}: {member.data[key]}")
                new_value = input(f"Enter new value for {key}: ").strip()
                member.set_stat(key, new_value)
                return
            else:
                print(f"Key '{key}' not found. Please try again.")
```

**Eliminates:**
- UI functions scattered in __main__.py (lines 130-442)
- Inconsistent prompt patterns

#### roster_strategy.py (Abstract Base)

```python
"""Abstract base class for roster type strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Optional, Tuple

class RosterStrategy(ABC):
    """Abstract base class defining interface for roster type operations."""

    @abstractmethod
    def get_roster_type_name(self) -> str:
        """Return human-readable roster type name."""
        pass

    @abstractmethod
    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return action dictionary for individual member operations."""
        pass

    @abstractmethod
    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return action dictionary for bulk team operations."""
        pass

    @abstractmethod
    def supports_name_search(self) -> bool:
        """Whether this roster type supports name-based search."""
        pass

    @abstractmethod
    def supports_bulk_operations(self) -> bool:
        """Whether this roster type supports bulk team operations."""
        pass

    @abstractmethod
    def get_name_keys(self) -> Optional[Tuple[str, str]]:
        """Return (first_name_key, last_name_key) tuple or None."""
        pass

    @abstractmethod
    def list_by_team(self, context, ui) -> None:
        """Display roster listing for a team (type-specific formatting)."""
        pass

    def get_skill_file_name(self) -> Optional[str]:
        """Return companion skill file name or None (optional override)."""
        return None

    def supports_name_randomization(self) -> bool:
        """Whether this roster type supports name randomization (optional override)."""
        return False
```

#### operations/player.py (Concrete Strategy)

```python
"""Player roster operations strategy."""

from typing import Dict, Callable, List, Tuple, Optional
import random
from ..roster_strategy import RosterStrategy
from ..models import Member, RosterContext
from ..constants import (
    MAXPLAYERSTAT, MAXHEALTH, MINPLRN,
    PLAYER_FIRST_NAME_CODE, PLAYER_LAST_NAME_CODE,
    PLAYER_STATS, PLAYER_POSITIONS
)

class PlayerStrategy(RosterStrategy):
    """Strategy for player roster operations."""

    def get_roster_type_name(self) -> str:
        return "Player"

    def get_name_keys(self) -> Tuple[str, str]:
        return (PLAYER_FIRST_NAME_CODE, PLAYER_LAST_NAME_CODE)

    def supports_name_search(self) -> bool:
        return True

    def supports_bulk_operations(self) -> bool:
        return True

    def supports_name_randomization(self) -> bool:
        return True

    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return player individual action dictionary."""
        return {
            "1": ("Maximize Potential", self.max_potential),
            "2": ("Maximize Health", self.max_health),
            "3": ("Resign for Peanuts (7yr contract at league minimum)", self.resign_for_peanuts),
            "4": ("Make Physical Specimen (increase size & potentials)", self.make_physical_specimen),
            "5": ("Take 'roids (inflate current stats)", self.inflate_current_stats),
            "6": ("Rename Player", self.rename_player),
            "7": ("Change Key Value", self.change_key_value),
        }

    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return player bulk action dictionary."""
        return {
            "1": ("Maximize Potential", self.max_potential),
            "2": ("Maximize Health", self.max_health),
            "3": ("Resign for Peanuts", self.resign_for_peanuts),
            "4": ("Make Physical Specimen", self.make_physical_specimen),
            "5": ("Take 'roids", self.inflate_current_stats),
            "6": ("Change Key Value", self.change_key_value),
        }

    def list_by_team(self, context: RosterContext, ui) -> None:
        """Display player roster listing for a team."""
        team_id = ui.prompt_team_id()
        if not team_id:
            return

        team_members = context.get_members_by_team(team_id)
        if not team_members:
            print(f"No players found for team ID {team_id}.")
            return

        print("\nPlayer List:")
        line = ""
        for player in team_members:
            pos_num = player.data.get('PPOS', '')
            position = PLAYER_POSITIONS.get(pos_num, "Unknown")
            first_name = player.data.get(PLAYER_FIRST_NAME_CODE, '')
            last_name = player.data.get(PLAYER_LAST_NAME_CODE, '')
            display_str = f"{position} {first_name} {last_name}"
            if len(line) + len(display_str) > 80:
                print(line)
                line = ""
            line += f"{display_str:<25}\t"
        if line:
            print(line)

    # Operation methods (max_potential, max_health, etc.)
    # ... [Transfer existing logic from __main__.py with minor adaptations]
```

#### cli.py (Application Orchestration)

```python
"""Command-line interface orchestration."""

from typing import Optional
from .models import RosterContext
from .io_handler import IOHandler
from .ui import UI
from .operations import STRATEGY_REGISTRY

class Application:
    """Main application controller."""

    def __init__(self):
        self.io_handler = IOHandler()
        self.ui = UI()
        self.strategy_registry = STRATEGY_REGISTRY

    def run(self) -> None:
        """Main application entry point."""
        # Get input file
        file_path = self.ui.get_input_file_path()

        # Load roster data
        headers, members = self.io_handler.read_csv(file_path)

        # Detect roster type and get strategy
        strategy = self.strategy_registry.get_strategy(headers[0])
        roster_type = strategy.get_roster_type_name()
        print(f"Detected roster type: {roster_type}")

        # Load skill file if needed
        skill_members = None
        skill_headers = None
        skill_file_path = None
        skill_file_name = strategy.get_skill_file_name()
        if skill_file_name:
            skill_file_path = self.io_handler.find_skill_file(file_path, skill_file_name)
            if skill_file_path:
                print(f"{skill_file_name} found at {skill_file_path}!")
                skill_headers, skill_members = self.io_handler.read_csv(skill_file_path)
            else:
                print(f"{skill_file_name} not found. Positional editing not possible.")

        # Create context
        context = RosterContext(
            roster_type=roster_type,
            members=members,
            headers=headers,
            file_path=file_path,
            skill_members=skill_members,
            skill_headers=skill_headers,
            skill_file_path=skill_file_path
        )

        # Run main menu loop
        self.main_menu(context, strategy)

        # Save changes if needed
        if context.changes_made:
            self.save_changes(context)

    def main_menu(self, context: RosterContext, strategy) -> None:
        """Main menu loop."""
        while True:
            print(f"\n=== Main Menu: {context.roster_type} Roster ===")

            menu_options = []
            if strategy.supports_name_search():
                menu_options.append(f"1. List all {context.roster_type}s on a team")
                menu_options.append(f"2. Select a {context.roster_type} by name")

            if strategy.supports_bulk_operations():
                menu_options.append(f"3. Modify all {context.roster_type}s on a team")
            else:
                menu_options.append(f"1. Select a {context.roster_type} by team")

            if strategy.supports_name_randomization():
                menu_options.append(f"4. Randomize {context.roster_type} names (all members)")

            menu_options.append("q. Quit")

            for option in menu_options:
                print(option)

            choice = input("\nEnter your choice: ").strip().lower()

            if choice in ['q', 'quit']:
                break
            elif choice == '1' and strategy.supports_name_search():
                strategy.list_by_team(context, self.ui)
            elif choice == '2' and strategy.supports_name_search():
                self.select_by_name(context, strategy)
            elif choice == '3' and strategy.supports_bulk_operations():
                self.modify_team(context, strategy)
            elif choice == '1' and not strategy.supports_name_search():
                self.select_by_team(context, strategy)
            elif choice == '4' and strategy.supports_name_randomization():
                self.randomize_names(context, strategy)
            else:
                print("Invalid choice. Please try again.")

    def save_changes(self, context: RosterContext) -> None:
        """Prompt to save changes."""
        if self.ui.confirm_save(context.file_path):
            output_file = self.io_handler.write_csv(context.members, context.headers, context.file_path)
            print(f"Changes saved to {output_file}")

            if context.skill_file_path and context.skill_members:
                skill_output = self.io_handler.write_csv(
                    context.skill_members,
                    context.skill_headers,
                    context.skill_file_path
                )
                print(f"Skill file changes saved to {skill_output}")
        else:
            print("Changes not saved.")

def main() -> None:
    """Entry point for the application."""
    app = Application()
    app.run()
```

---

## Part 3: Migration Strategy

### 3.1 Phased Implementation Approach

**Goal:** Refactor without breaking existing functionality. Each phase should be independently testable.

#### Phase 1: Foundation (No Breaking Changes)

**Objective:** Create new modules without modifying __main__.py.

| Step | Action | Files Created | Validation |
|:-----|:-------|:--------------|:-----------|
| 1.1 | Create `constants.py` | constants.py | Import in test script, verify values |
| 1.2 | Create `models.py` | models.py | Unit tests for Member, RosterContext |
| 1.3 | Create `io_handler.py` | io_handler.py | Test read/write with sample CSV |
| 1.4 | Create `ui.py` | ui.py | Manual testing of prompts |

**Success Criteria:**
- All new modules import successfully
- Unit tests pass
- No changes to __main__.py
- Original script still works

#### Phase 2: Strategy Pattern (Parallel Implementation)

**Objective:** Implement strategy pattern alongside existing code.

| Step | Action | Files Created | Validation |
|:-----|:-------|:--------------|:-----------|
| 2.1 | Create `roster_strategy.py` | roster_strategy.py | Abstract base imports |
| 2.2 | Create `operations/player.py` | operations/player.py | Player operations work |
| 2.3 | Create `operations/coach.py` | operations/coach.py | Coach operations work |
| 2.4 | Create `operations/gm.py` | operations/gm.py | GM operations work |
| 2.5 | Create `operations/trainer.py` | operations/trainer.py | Trainer operations work |
| 2.6 | Create `operations/__init__.py` | operations/__init__.py | Registry works |

**Success Criteria:**
- All strategies implement complete interface
- Strategy registry correctly maps headers
- Individual operation functions work
- Original __main__.py still works

#### Phase 3: CLI Orchestration (Parallel Implementation)

**Objective:** Implement new CLI orchestration without modifying __main__.py.

| Step | Action | Files Created | Validation |
|:-----|:-------|:--------------|:-----------|
| 3.1 | Create `cli.py` | cli.py | New CLI works end-to-end |
| 3.2 | Create new `__main__.py` (temporary name) | __main_new__.py | Entry point works |
| 3.3 | Test new implementation thoroughly | N/A | All features work |

**Success Criteria:**
- New CLI provides all features of old CLI
- No regressions in functionality
- Context passing works correctly
- No global state used

#### Phase 4: Cutover (Breaking Change)

**Objective:** Replace old __main__.py with new modular architecture.

| Step | Action | Files Modified | Validation |
|:-----|:-------|:---------------|:-----------|
| 4.1 | Rename old __main__.py | __main_legacy__.py | Backup exists |
| 4.2 | Rename __main_new__.py | __main__.py | New entry point active |
| 4.3 | Update __init__.py exports | __init__.py | Package imports work |
| 4.4 | Comprehensive testing | N/A | All features work |

**Success Criteria:**
- All tests pass
- Manual testing confirms feature parity
- No regressions identified
- Documentation updated

#### Phase 5: Cleanup (Polish)

**Objective:** Remove legacy code, add type hints, improve documentation.

| Step | Action | Files Modified | Validation |
|:-----|:-------|:---------------|:-----------|
| 5.1 | Delete __main_legacy__.py | __main_legacy__.py | No dependencies remain |
| 5.2 | Add type hints to all modules | All .py files | mypy passes |
| 5.3 | Add docstrings | All .py files | Documentation complete |
| 5.4 | Update CLAUDE.md | CLAUDE.md | Reflects new architecture |

**Success Criteria:**
- No legacy code remains
- Type hints complete
- Documentation accurate
- Code quality metrics improved

### 3.2 Testing Strategy

**Test Coverage Required:**

| Module | Test Type | Priority | Coverage Target |
|:-------|:----------|:---------|:----------------|
| constants.py | Unit | Medium | 100% (trivial) |
| models.py | Unit | High | 95%+ |
| io_handler.py | Integration | High | 90%+ |
| ui.py | Manual | Medium | N/A (interactive) |
| roster_strategy.py | Unit | High | 100% (abstract) |
| operations/player.py | Unit | Critical | 95%+ |
| operations/coach.py | Unit | Critical | 95%+ |
| operations/gm.py | Unit | High | 90%+ |
| operations/trainer.py | Unit | High | 90%+ |
| cli.py | Integration | Critical | 85%+ |

**Test Fixtures Needed:**
- Sample player CSV (10 players, 2 teams)
- Sample coach CSV (5 coaches, 1 team)
- Sample GM CSV (1 GM)
- Sample trainer CSV (1 trainer)
- Sample cskl.csv (coach skills)
- Sample gmsk.csv (GM skills)

**Regression Test Checklist:**
1. Load each roster type (Player, Coach, GM, Trainer)
2. Detect roster type correctly
3. List roster by team
4. Select member by name (Player, Coach)
5. Select member by team (GM, Trainer)
6. Apply individual operations
7. Apply bulk operations
8. Randomize names (Player, Coach)
9. Save changes to new file
10. Load companion skill files (Coach, GM)
11. Modify skill file data
12. Save skill file changes

### 3.3 Backward Compatibility Considerations

**Public API Stability:**
- Entry point remains `python -m hc09_db_csv_editor [file]`
- CLI behavior unchanged (same menus, same prompts)
- Output file naming unchanged (_modified suffix)
- CSV format unchanged

**Breaking Changes (Internal Only):**
- Module imports change (for anyone importing internals)
- Global variables removed (shouldn't have been used externally)
- Function signatures change (internal refactor)

**Mitigation:**
- Keep __main_legacy__.py available for one release cycle
- Document migration in CHANGELOG
- Update CLAUDE.md with new architecture

---

## Part 4: Implementation Checklist

### 4.1 File Creation Order

**Critical Path (must be done in order):**

```
1. constants.py       (no dependencies)
2. models.py          (depends on constants)
3. io_handler.py      (depends on models, constants)
4. ui.py              (depends on models, constants)
5. roster_strategy.py (depends on models)
6. operations/player.py    (depends on roster_strategy, models, constants)
7. operations/coach.py     (depends on roster_strategy, models, constants)
8. operations/gm.py        (depends on roster_strategy, models, constants)
9. operations/trainer.py   (depends on roster_strategy, models, constants)
10. operations/__init__.py (depends on all operations)
11. cli.py            (depends on all modules)
12. __main__.py       (depends on cli)
13. __init__.py       (updated to export public API)
```

### 4.2 Code Transfer Mapping

**From __main__.py to new modules:**

| Lines | Current Location | Target Module | Target Function/Class |
|:------|:----------------|:--------------|:---------------------|
| 8-98 | Constants section | constants.py | Module-level constants |
| 102-104 | Global variables | models.py | RosterContext class |
| 108-126 | Member class | models.py | Member class (refactored) |
| 130-143 | get_input_file | ui.py | UI.get_input_file_path() |
| 146-219 | main_menu | cli.py | Application.main_menu() |
| 221-229 | read_members_from_csv | io_handler.py | IOHandler.read_csv() |
| 232-242 | save_changes_confirmation | cli.py | Application.save_changes() |
| 245-257 | write_members_to_csv | io_handler.py | IOHandler.write_csv() |
| 261-263 | captain_personality | operations/[all] | As individual method |
| 265-277 | change_key_value | ui.py | UI.prompt_key_value_change() |
| 280-290 | detect_roster_type | operations/__init__.py | StrategyRegistry logic |
| 293-314 | find_member_by_team | cli.py | Application.select_by_team() |
| 317-331 | find_member_index | cli.py | Helper method |
| 334-347 | find_skill_file | io_handler.py | IOHandler.find_skill_file() |
| 350-355 | list_roster_by_team | cli.py | Delegates to strategy |
| 358-380 | modify_member | cli.py | Application.modify_individual() |
| 382-403 | modify_bulk_members | cli.py | Application.modify_bulk() |
| 406-411 | modify_roster_member | cli.py | Delegates to strategy |
| 414-421 | modify_team_roster | cli.py | Application.modify_team() |
| 424-425 | read_the_manual | operations/[all] | As individual method |
| 428-441 | print_team_names | ui.py | UI.print_team_names() |
| 446-458 | inflate_current_stats | operations/player.py | PlayerStrategy.inflate_current_stats() |
| 461-513 | list_players_by_team | operations/player.py | PlayerStrategy.list_by_team() |
| 516-527 | max_health | operations/player.py | PlayerStrategy.max_health() |
| 530-538 | max_potential | operations/player.py | PlayerStrategy.max_potential() |
| 541-551 | make_physical_specimen | operations/player.py | PlayerStrategy.make_physical_specimen() |
| 554-563 | modify_all_players_on_team | operations/player.py | Strategy integration |
| 565-575 | modify_player | operations/player.py | PlayerStrategy actions |
| 578-601 | randomize_player_names | operations/player.py | PlayerStrategy.randomize_names() |
| 604-608 | rename_player | operations/player.py | PlayerStrategy.rename_member() |
| 611-639 | resign_for_peanuts | operations/player.py | PlayerStrategy.resign_for_peanuts() |
| 643-685 | list_coaches_by_team | operations/coach.py | CoachStrategy.list_by_team() |
| 688-691 | max_general_coaching_potential | operations/coach.py | CoachStrategy.max_general_potential() |
| 694-704 | max_positional_coaching_potential | operations/coach.py | CoachStrategy.max_positional_potential() |
| 707-716 | modify_all_coaches_on_team | operations/coach.py | Strategy integration |
| 719-729 | modify_coach | operations/coach.py | CoachStrategy actions |
| 732-755 | randomize_coach_names | operations/coach.py | CoachStrategy.randomize_names() |
| 758-762 | rename_coach | operations/coach.py | CoachStrategy.rename_member() |
| 766-769 | max_general_gm_potential | operations/gm.py | GMStrategy.max_general_potential() |
| 772-782 | max_positional_gm_potential | operations/gm.py | GMStrategy.max_positional_potential() |
| 785-793 | modify_gm | operations/gm.py | GMStrategy actions |
| 795-796 | rename_gm | operations/gm.py | Placeholder |
| 800-803 | max_trainer_potential | operations/trainer.py | TrainerStrategy.max_trainer_potential() |
| 806-813 | modify_trainer | operations/trainer.py | TrainerStrategy actions |
| 816-817 | rename_trainer | operations/trainer.py | Placeholder |
| 821-832 | main() | __main__.py | Delegates to cli.main() |

### 4.3 Specific Refactoring Steps for python-pro

**Step-by-step implementation guide:**

#### Step 1: Create constants.py
```
Task: Extract all constants from __main__.py lines 8-98
- Copy constant definitions verbatim
- Add module docstring
- Organize into sections (stat limits, field keys, mappings)
- No logic changes required
```

#### Step 2: Create models.py
```
Task: Refactor Member class and create RosterContext
- Copy Member class (lines 108-126)
- Remove global roster_type dependency
- Add get_stat() method for consistency
- Refactor get_name() to accept name keys as parameters
- Create RosterContext class per design
- Add get_members_by_team() helper method
- Add comprehensive docstrings
```

#### Step 3: Create io_handler.py
```
Task: Extract I/O functions into IOHandler class
- Transfer read_members_from_csv (lines 221-229) -> read_csv()
- Transfer write_members_to_csv (lines 245-257) -> write_csv()
- Transfer find_skill_file (lines 334-347) -> find_skill_file()
- Add validate_file_path() helper
- Make all methods static (no instance state needed)
- Add comprehensive docstrings
```

#### Step 4: Create ui.py
```
Task: Extract UI functions into UI class
- Transfer get_input_file (lines 130-143) -> get_input_file_path()
- Transfer print_team_names (lines 428-441) -> print_team_names()
- Create prompt_team_id() (extract from various locations)
- Create prompt_name() (extract from lines 170-175)
- Transfer change_key_value logic (lines 265-277) -> prompt_key_value_change()
- Create display_action_menu() (extract pattern from modify_member/modify_bulk_members)
- Create confirm_save() (extract from save_changes_confirmation lines 232-242)
- Make all methods static
- Add comprehensive docstrings
```

#### Step 5: Create roster_strategy.py
```
Task: Define abstract base class for strategies
- Create RosterStrategy abstract base class
- Define abstract methods per design
- Add docstrings explaining contract
- No concrete implementations yet
```

#### Step 6: Create operations/player.py
```
Task: Implement PlayerStrategy
- Create PlayerStrategy class extending RosterStrategy
- Transfer player functions (lines 446-640)
- Implement all abstract methods
- Convert functions to methods (add self parameter)
- Add context parameter where needed
- Update to use constants from constants.py
- Remove global variable dependencies
- Add comprehensive docstrings
```

#### Step 7: Create operations/coach.py
```
Task: Implement CoachStrategy
- Create CoachStrategy class extending RosterStrategy
- Transfer coach functions (lines 643-763)
- Follow same pattern as PlayerStrategy
- Implement skill file operations
- Add comprehensive docstrings
```

#### Step 8: Create operations/gm.py
```
Task: Implement GMStrategy
- Create GMStrategy class extending RosterStrategy
- Transfer GM functions (lines 766-797)
- Follow same pattern as CoachStrategy
- Implement skill file operations
- Add comprehensive docstrings
```

#### Step 9: Create operations/trainer.py
```
Task: Implement TrainerStrategy
- Create TrainerStrategy class extending RosterStrategy
- Transfer trainer functions (lines 800-817)
- Simpler than other strategies (no name search, no bulk ops)
- Add comprehensive docstrings
```

#### Step 10: Create operations/__init__.py
```
Task: Create strategy registry
- Import all strategy classes
- Create StrategyRegistry class
- Map headers to strategy instances
- Export STRATEGY_REGISTRY singleton
- Add comprehensive docstrings
```

#### Step 11: Create cli.py
```
Task: Implement application orchestration
- Create Application class
- Transfer main_menu logic (lines 146-219)
- Implement helper methods (select_by_name, select_by_team, modify_team, etc.)
- Replace global state with context passing
- Integrate strategy pattern
- Replace direct function calls with strategy method calls
- Add comprehensive docstrings
```

#### Step 12: Update __main__.py
```
Task: Replace with minimal entry point
- Import cli.main
- Call cli.main() in if __name__ == "__main__" block
- Remove all other code (will be preserved in backup)
- Add docstring
```

#### Step 13: Update __init__.py
```
Task: Update package exports
- Define __version__
- Export public API (Application, main)
- Add __all__ list
- Update docstring
```

### 4.4 Validation Checklist

After each phase, verify:

- [ ] All modules import successfully
- [ ] No circular import dependencies
- [ ] Unit tests pass (where applicable)
- [ ] Manual testing confirms functionality
- [ ] No regressions identified
- [ ] Code follows CLAUDE.md conventions
- [ ] Docstrings are comprehensive
- [ ] Type hints added (if applicable)
- [ ] No global state dependencies
- [ ] Context passing works correctly

---

## Part 5: Benefits Summary

### 5.1 Code Quality Improvements

| Metric | Before | After | Improvement |
|:-------|:-------|:------|:-----------|
| **Lines per file** | 833 (1 file) | ~100 avg (9 files) | 8x reduction |
| **Cyclomatic complexity** | High (nested loops/conditions) | Low (single responsibility) | 60% reduction |
| **Global variables** | 3 | 0 | 100% elimination |
| **Function cohesion** | Low (mixed concerns) | High (single responsibility) | Significant |
| **Testability** | Low (global state) | High (dependency injection) | 10x improvement |
| **Code duplication** | High (4 similar patterns) | Low (strategy pattern) | 75% reduction |
| **Type safety** | None (no hints) | Full (comprehensive hints) | 100% coverage |

### 5.2 Maintainability Improvements

**Easier to:**
- Add new roster types (just implement strategy interface)
- Modify individual operations (isolated in strategy)
- Change UI behavior (isolated in ui.py)
- Add new I/O formats (isolated in io_handler.py)
- Write unit tests (no global state)
- Navigate codebase (clear module boundaries)
- Understand architecture (explicit dependencies)
- Onboard new developers (better documentation)

### 5.3 Extensibility Improvements

**Future enhancements made easier:**
- Add PERV file support for GM/Trainer renaming (add to io_handler)
- Batch processing mode (extend Application class)
- Configuration file support (add config module)
- Undo/redo functionality (add command pattern layer)
- Export operation history (add logging to context)
- GUI frontend (reuse strategy/models/io layers)
- REST API (reuse all layers except ui/cli)

### 5.4 Alignment with CLAUDE.md Vision

**Addresses all future considerations:**
- ✅ Extract Member class to models.py
- ✅ Extract operations to operations/ directory
- ✅ Extract IO functions to io_handler.py
- ✅ Extract UI functions to ui.py
- ✅ Refactor action dictionaries into strategy pattern
- ✅ Add type hints (Phase 5)
- ⚠️ CSV schema validation (future enhancement)
- ⚠️ Logging instead of print (future enhancement)

---

## Part 6: Risk Assessment

### 6.1 Implementation Risks

| Risk | Probability | Impact | Mitigation |
|:-----|:-----------|:-------|:----------|
| **Breaking existing functionality** | Medium | High | Phased implementation, keep legacy backup |
| **Incomplete migration** | Low | High | Comprehensive checklist, validation at each phase |
| **Performance regression** | Low | Low | Benchmark before/after, optimize if needed |
| **Circular import dependencies** | Medium | Medium | Careful dependency design, test imports early |
| **Context passing overhead** | Low | Low | Python object passing is cheap, not a real concern |
| **Testing gaps** | Medium | Medium | Comprehensive test plan, regression checklist |

### 6.2 Mitigation Strategies

1. **Parallel Implementation:** Build new architecture alongside old (Phases 1-3)
2. **Backup Preservation:** Keep __main_legacy__.py for rollback
3. **Incremental Validation:** Test after each phase, not just at end
4. **Regression Testing:** Comprehensive manual testing checklist
5. **Documentation Updates:** Keep CLAUDE.md in sync with changes

---

## Part 7: Success Criteria

### 7.1 Functional Requirements

- [ ] All roster types work (Player, Coach, GM, Trainer)
- [ ] All individual operations work
- [ ] All bulk operations work
- [ ] Name search works (Player, Coach)
- [ ] Team search works (GM, Trainer)
- [ ] Name randomization works (Player, Coach)
- [ ] Skill file loading works (Coach, GM)
- [ ] Skill file modification works
- [ ] Save functionality works (incremental naming)
- [ ] Quit without save works
- [ ] Invalid input handled gracefully

### 7.2 Non-Functional Requirements

- [ ] No global variables used
- [ ] All modules have clear single responsibilities
- [ ] No code duplication (DRY principle)
- [ ] Type hints on all public functions
- [ ] Docstrings on all modules, classes, public functions
- [ ] No circular dependencies
- [ ] Import time < 500ms
- [ ] Memory usage unchanged
- [ ] Performance within 10% of original

### 7.3 Code Quality Requirements

- [ ] CLAUDE.md conventions followed
- [ ] Line length < 120 characters
- [ ] No print statements (replaced with proper output abstraction)
- [ ] Consistent naming conventions
- [ ] Comprehensive error handling
- [ ] Clear separation of concerns
- [ ] Strategy pattern correctly implemented
- [ ] Dependency injection used throughout

---

## Conclusion

This refactoring plan provides a comprehensive roadmap for transforming the monolithic __main__.py into a clean, modular architecture. The Strategy Pattern with dependency injection eliminates global state, improves testability, and establishes a foundation for future extensibility.

**Estimated Effort:**
- Phase 1 (Foundation): 4-6 hours
- Phase 2 (Strategy Pattern): 8-10 hours
- Phase 3 (CLI Orchestration): 4-6 hours
- Phase 4 (Cutover): 2-3 hours
- Phase 5 (Cleanup): 3-4 hours
- **Total: 21-29 hours**

**Next Steps:**
1. Review this plan with stakeholders
2. Create test fixtures for validation
3. Begin Phase 1 implementation
4. Validate each phase before proceeding
5. Document learnings for future refactors

---

**Document Status:** Ready for Implementation
**Approved By:** [Pending Review]
**Implementation Start Date:** [TBD]
