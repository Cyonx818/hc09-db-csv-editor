---
audience: user
---

# Usage Guide

> **Purpose:** Comprehensive guide to all operations available in the NFL Head Coach '09 CSV Editor.
> **Audience:** Users familiar with basic operation who want to master all features.

## Table of Contents

1. [Roster Types](#roster-types)
2. [Player Operations](#player-operations)
3. [Coach Operations](#coach-operations)
4. [GM Operations](#gm-operations)
5. [Trainer Operations](#trainer-operations)
6. [Bulk vs Individual Editing](#bulk-vs-individual-editing)
7. [Advanced Techniques](#advanced-techniques)

## Roster Types

The tool automatically detects which roster type you're editing:

| Type | Detection Header | Features |
|------|------------------|----------|
| **Player** | `PSA0` | Full suite: individual, bulk, name operations |
| **Coach** | `CFDA` | Requires `cskl.csv` for positional skills |
| **GM** | `GMAB` | Requires `gmsk.csv` for positional skills |
| **Trainer** | `TRAB` | Limited operations (no name editing) |

## Player Operations

### 1. Maximize Potential

**What it does:** Sets all potential stats (ending in 'x' or 'X') to maximum values.

**Use cases:**
- Create future superstars for franchise mode
- Develop young players into hall-of-famers
- Balance rosters by equalizing potential

**Stats affected:** All potential ratings (PSDX, PAGX, PACX, PSTX, etc.)

**Limits applied:**
- Normal stats: 99 (MAXPLAYERSTAT)
- Health stats: 1000 (MAXHEALTH)

**Example:**
```
Player: QB with 85 Speed Potential (PSDX)
Action: Maximize Potential
Result: Speed Potential (PSDX) = 99
```

### 2. Maximize Health

**What it does:** Sets injury, durability, and stamina stats to maximum.

**Use cases:**
- Heal all injuries instantly
- Prevent future injuries
- Extend career longevity

**Stats affected:**
- Injury ratings: `PLAC`, `PRAC`, `PHDC`, `PLLC`, `PTRC`, `PRLc`
- Stamina: `PSTA`
- Toughness: `PTGH`, `PINJ`
- Learning: `PLRN` (minimum 75 if below)

**Example:**
```
Player: RB with knee injury (PLLC = 50)
Action: Maximize Health
Result: All health stats = 99, knee = 99, learning minimum 75
```

### 3. Resign for Peanuts

**What it does:** Adjusts contract to 7 years at league minimum salary.

**Use cases:**
- Salary cap management
- Sign entire team affordably
- Keep superstars under budget

**Contract fields modified:**
- Salary years (PSA0-PSA6): 24 (league minimum)
- Bonuses (PSB0-PSB6): 0
- Contract length (PCYL, PCON): 7 years
- Personality (PTId): 9 (Captain - more accepting)

**Warning:** This creates an unrealistic contract. Some leagues may flag this.

### 4. Make Physical Specimen

**What it does:** Increases physical attributes and resets age to 21.

**Use cases:**
- Create physically dominant players
- Reset veteran's age for extended career
- Build prototypical position players

**Changes:**
- Age (PAGE): Set to 21
- Height (PHGT): +10%
- Weight (PWGT): +10%

**Example:**
```
Player: 30-year-old QB, 6'2" (74 inches), 220 lbs
Action: Make Physical Specimen
Result: 21-year-old QB, 6'8" (81 inches), 242 lbs
```

### 5. Take 'roids (Inflate Current Stats)

**What it does:** Increases current stats by 50% of the gap between current and potential.

**Use cases:**
- Instant improvement without waiting for development
- Bring players up to half their potential
- Quick roster upgrades mid-season

**Formula:**
```
New Stat = Current + (Potential - Current) / 2
```

**Example:**
```
Player: Speed 70, Speed Potential 90
Calculation: 70 + (90 - 70) / 2 = 70 + 10 = 80
Result: Speed = 80
```

**Note:** Only affects stats below potential. Already-maxed stats unchanged.

### 6. Rename Player

**What it does:** Changes player's first and last name.

**Use cases:**
- Create custom rosters
- Replace real names with generic names
- Personalize franchise rosters

**Case-sensitive:** Names must match game's name database casing for proper display.

### 7. Change Key Value

**What it does:** Manually edit any 4-character CSV field.

**Use cases:**
- Advanced editing of specific attributes
- Modify fields not covered by other operations
- Fine-tune player ratings

**Requirements:**
- Key must be exactly 4 characters
- Key must exist in player's data
- Case-sensitive

**Example:**
```
Enter key name: PSPD
Current value for PSPD: 85
Enter new value: 95
```

**Warning:** Changing unknown keys can corrupt rosters. See [CSV Reference](../reference/csv-fields.md) for field documentation.

## Coach Operations

### 1. Max General Coaching Potential

**What it does:** Maximizes core coaching attributes.

**Stats affected:** `SKPA`, `SKCM`, `SKSM`, `SKPX`

**Limit:** 5 (MAXCOACHSTAT)

### 2. Max Positional Coaching Potential

**What it does:** Maximizes position-specific coaching skills.

**Requirements:** `cskl.csv` file in same directory as coach CSV.

**Stats affected:** `SKIM`, `SKPM`, `SKLM` (in cskl.csv)

**Warning:** Tool warns if `cskl.csv` not found. Operation skipped if unavailable.

### 3. Read the Manual (Max Skill Points)

**What it does:** Sets skill points to maximum (131,000).

**Use case:** Unlock all coach skill trees instantly.

**Field:** `SKPT` = 131000

### 4. Take Old Boy Out for Drinks (Captain Personality)

**What it does:** Sets personality trait to "Captain" (most agreeable).

**Use case:** Reduce coach complaints and improve morale.

**Field:** `PTId` = 9

### 5. Rename Coach

**What it does:** Changes coach's first and last name.

**Fields:** `CFNM` (first name), `CLNM` (last name)

## GM Operations

GM operations mirror coach operations but with GM-specific skill fields.

### 1. Max General GM Potential

**Stats affected:** `SKTM`, `SKTD`, `SKNM`, `SKNG`

### 2. Max Positional GM Potential

**Requirements:** `gmsk.csv` file in same directory.

**Stats affected:** `SKRM`, `SKSX` (in gmsk.csv)

### 3-4. Skill Points and Personality

Same as coach operations (fields: `SKPT`, `PTId`).

**Note:** GM renaming requires PERV file (not yet implemented).

## Trainer Operations

### 1. Max Trainer Potential

**Stats affected:** `TSIM`, `TSRM`, `TSFM`

**Limit:** 5 (MAXGMSTAT)

### 2-3. Skill Points and Personality

Same as coach/GM operations.

**Note:** Trainer renaming requires PERV file (not yet implemented).

## Bulk vs Individual Editing

### Individual Editing

**Access:** Main Menu → Option 2

**Workflow:**
1. Enter first name
2. Enter last name
3. Tool finds player
4. Action menu appears
5. Apply operations
6. Return to main menu or select another player

**Best for:**
- Editing specific star players
- Precise control over changes
- Testing operations before bulk use

### Bulk Editing

**Access:** Main Menu → Option 3

**Workflow:**
1. View team list
2. Enter team ID (1-33)
3. Action menu appears
4. Apply operation
5. ALL players on team affected simultaneously

**Best for:**
- Roster-wide improvements
- Salary cap fixes
- Healing entire team
- Franchise mode team building

**Warning:** Bulk operations cannot be undone except by reloading original CSV. Use cautiously.

### Team ID Reference

| ID | Team | ID | Team |
|----|------|----|------|
| 01 | Bears | 17 | Jaguars |
| 02 | Bengals | 18 | Jets |
| 03 | Bills | 19 | Lions |
| 04 | Broncos | 20 | Packers |
| 05 | Browns | 21 | Panthers |
| 06 | Buccaneers | 22 | Patriots |
| 07 | Cardinals | 23 | Raiders |
| 08 | Chargers | 24 | Rams |
| 09 | Chiefs | 25 | Ravens |
| 10 | Colts | 26 | Redskins |
| 11 | Cowboys | 27 | Saints |
| 12 | Dolphins | 28 | Seahawks |
| 13 | Eagles | 29 | Steelers |
| 14 | Falcons | 30 | Texans |
| 15 | 49ers | 31 | Titans |
| 16 | Giants | 32 | Vikings |
| **33** | **Free Agents** | - | - |

**Special:** Team ID 33 represents all players not assigned to a team (free agents, practice squad).

## Advanced Techniques

### Creating Custom Draft Classes

1. Export player roster
2. Identify rookies (age 21-22)
3. Maximize potential on all rookies
4. Inflate current stats by 25% (run "Take 'roids" twice on same player if needed)
5. Import modified roster

### Salary Cap Emergency Fix

When over cap and unable to sign players:

1. Export player roster
2. Bulk edit team → "Resign for Peanuts"
3. Import roster
4. Renegotiate key players in-game to realistic contracts

### Balancing Competitive Franchise

Make all teams equally competitive:

1. Export player roster
2. For each team ID (1-32):
   - Bulk edit → Maximize Potential
3. Start franchise with all teams having equal potential
4. Let in-game development create variance

### Name Randomization Uses

The "Randomize names" feature shuffles first/last names:

**Use cases:**
- Create generic rosters (avoid real player names)
- Add variety to auto-generated draft classes
- Test tool without modifying real rosters

**How it works:**
1. Collects all unique first names
2. Collects all unique last names
3. Randomly assigns new first/last combinations to each player

**Warning:** This affects ALL players in the file. Cannot undo except by reloading original.

### Multi-File Workflows

HC09 uses multiple roster files. For complete roster overhaul:

1. Export all roster types (players, coaches, GMs, trainers)
2. Edit each file separately
3. Import all modified files together
4. Verify in-game consistency

### Backup and Version Control

**Recommended workflow:**
1. Export CSV → `roster_v1.csv`
2. Edit with tool → `roster_v1_modified.csv`
3. Copy to `roster_v2.csv` (new baseline)
4. Make more changes → `roster_v2_modified.csv`
5. Keep all versions for rollback

This preserves edit history and allows selective rollback.

## Best Practices

1. **Test on one player first:** Verify operation works as expected
2. **Backup before bulk:** Save original CSV before team-wide changes
3. **Review modified file:** Open in text editor to verify changes
4. **Import incrementally:** Test modified roster in-game before making more changes
5. **Document changes:** Keep notes on what you modified for future reference

## Next Steps

- **Field reference:** See [CSV Fields Reference](../reference/csv-fields.md) for complete field documentation
- **Troubleshooting:** Check [Common Issues](troubleshooting.md) if operations fail
- **Examples:** Review [Usage Examples](../examples/common-scenarios.md) for specific scenarios
