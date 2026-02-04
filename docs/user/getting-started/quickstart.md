---
audience: user
---

# Quick Start Guide

> **Purpose:** Get started editing your first NFL Head Coach '09 roster in under 10 minutes.
> **Prerequisites:** [Installation](installation.md) completed

## Overview

This guide walks you through a complete editing session:
1. Export CSV from your save game
2. Open the CSV in the editor
3. Make changes to a player
4. Save the modified file
5. Import back to your save game

## Step 1: Export CSV from HC09

You'll need a save game editor that can export roster databases to CSV format. Common tools include:
- NFL Head Coach 09 Editor
- Universal Game Editor
- Custom roster export tools

**Export one of these roster types:**
- **Player roster** (`plyr.csv` or similar)
- **Coach roster** (`coch.csv` or similar)
- **GM roster** (`genm.csv` or similar)
- **Trainer roster** (`tran.csv` or similar)

Save the exported CSV to a known location (e.g., `C:\HC09\exports\players.csv`).

## Step 2: Launch the Editor

**If installed with pip:**

```bash
hc09-editor C:\HC09\exports\players.csv
```

Or run without arguments and enter the path when prompted:

```bash
hc09-editor
Enter the path to the input CSV file: C:\HC09\exports\players.csv
```

**If running without installation:**

Open a terminal in the `hc09-db-csv-editor` directory and run:

```bash
# Option A: Run from src directory
cd src
python -m hc09_db_csv_editor C:\HC09\exports\players.csv

# Option B: Run __main__.py directly
python src/hc09_db_csv_editor/__main__.py C:\HC09\exports\players.csv
```

Or run without arguments and enter the path when prompted:

```bash
# From src directory
cd src
python -m hc09_db_csv_editor
Enter the path to the input CSV file: C:\HC09\exports\players.csv
```

## Step 3: Detect Roster Type

The tool automatically detects the roster type:

```
Detected roster type: Player
```

You'll see a main menu appropriate for the detected type.

## Step 4: Make Your First Edit

### Example: Maximize a Player's Potential

```
Main Menu:
1. List all Players on a team
2. Select a Player by name
3. Modify all Players on a team
4. Randomize Players names (warning, this will affect all Players!)
q. Quit

Enter your choice: 2
```

Enter the player's name:

```
Enter Player's first name (or 'q' to quit): Tom
Enter Player's last name (or 'q' to quit): Brady
```

Choose an action:

```
Choose an action to perform:
1. Maximize Potential
2. Maximize Health
3. Resign for Peanuts (7yr contract at league minimum salary)
4. Make Physical Specimen (increase physical size & max potentials)
5. Take 'roids (inflate current stats)
6. Rename Player
7. Change Key Value
q. Quit to player selection

Enter the number of your choice: 1
```

The tool confirms:

```
Action 'Maximize Potential' performed on player.
```

## Step 5: Save Changes

Return to the main menu (press `q`) and quit:

```
Enter the number of your choice: q
Do you want to save changes to C:\HC09\exports\players.csv? (yes/no): yes
Changes saved to C:\HC09\exports\players_modified.csv
```

**Important:** The original file is preserved. The modified data is in `players_modified.csv`.

## Step 6: Import Modified CSV

Use your save game editor to import `players_modified.csv` back into your HC09 save game.

## Common First-Time Operations

### Boost an Entire Team

Perfect for franchise mode with your favorite team:

```
Main Menu: 3
Enter team to bulk edit Players: 22  # Patriots
Choose action: 1  # Maximize Potential
```

This maximizes all Patriots players' potential stats.

### Fix Injured Players

Heal all injuries on a team:

```
Main Menu: 3
Enter team to bulk edit Players: 22
Choose action: 2  # Maximize Health
```

### Create Superstar Contracts

Make all players on a team sign cheap contracts:

```
Main Menu: 3
Enter team to bulk edit Players: 22
Choose action: 3  # Resign for Peanuts
```

## Understanding the Menu Structure

```
Main Menu
├── Option 1: List all [Type]s on a team
│   └── Shows roster by position for a selected team
├── Option 2: Select a [Type] by name
│   └── Edit individual roster member
│       └── Action menu (varies by type)
├── Option 3: Modify all [Type]s on a team
│   └── Bulk operations on entire team roster
│       └── Action menu (same actions as individual)
└── Option 4: Randomize names
    └── Shuffles first/last names across all roster members
```

## Tips for First-Time Users

1. **Start with one player:** Get comfortable with individual edits before bulk operations
2. **Backup your save:** Always keep an unmodified copy of your original CSV
3. **Test changes:** Import modified CSV and verify in-game before making more changes
4. **Explore team lists:** Use Option 1 to browse rosters and find player names
5. **Read warnings:** The name randomization warning is serious - it affects ALL roster members

## Next Steps

- **Learn all operations:** See [Usage Guide](../guides/usage.md) for complete operation details
- **Understand CSV fields:** Review [CSV Reference](../reference/csv-fields.md) for advanced editing
- **Troubleshooting:** Check [Common Issues](../guides/troubleshooting.md) if you encounter problems

## Quick Reference Card

| Task | Menu Path |
|------|-----------|
| **Launch editor** | `hc09-editor roster.csv` (or `python src/hc09_db_csv_editor/__main__.py roster.csv`) |
| Edit one player | Main → 2 → Enter name → Choose action |
| Edit whole team | Main → 3 → Enter team ID → Choose action |
| View team roster | Main → 1 → Enter team ID |
| Randomize names | Main → 4 → Confirm |
| Save and exit | Main → q → yes |
| Exit without saving | Main → q → no |
