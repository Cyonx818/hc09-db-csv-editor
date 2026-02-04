---
audience: user
---

# CSV Fields Reference

> **Purpose:** Complete reference for NFL Head Coach '09 CSV field codes.
> **Audience:** Advanced users performing custom edits with "Change Key Value" operation.
> **Warning:** Modifying fields incorrectly can corrupt rosters. Use with caution.

## Field Naming Convention

All CSV fields use **4-character codes** that are **case-sensitive**.

### Code Patterns

- **P-prefix:** Player fields (e.g., `PSPD`, `PAGE`)
- **C-prefix:** Coach fields (e.g., `CFNM`, `COPS`)
- **G/GM-prefix:** GM fields (e.g., `GMAB`, `SKTM`)
- **T-prefix:** Trainer/Team fields (e.g., `TGID`, `TSIM`)
- **SK-prefix:** Skill fields (e.g., `SKPT`, `SKPA`)

### Potential vs Current Stats

Many player stats have paired fields:

- **Current stat:** 4-char code (e.g., `PSPD` = Speed)
- **Potential (max):** Same code + 'X' (e.g., `PSDX` = Speed Potential)

**Example:**
```
PSPD: 85  (current speed)
PSDX: 92  (maximum potential speed)
```

## Player Fields

### Identity Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `PFNA` | First Name | "Tom" |
| `PLNA` | Last Name | "Brady" |
| `PAGE` | Age | 21-40 |
| `PPOS` | Position Code | 0-20 (see Position Codes) |
| `TGID` | Team ID | 1-33 (see Team IDs) |
| `PNid` | Personnel ID | Unique identifier |

### Physical Attributes

| Field | Description | Range | Notes |
|-------|-------------|-------|-------|
| `PHGT` | Height | 60-90 | In inches (6'0" = 72) |
| `PWGT` | Weight | 150-400 | In pounds |

### Core Stats (Current/Potential Pairs)

| Current | Potential | Stat Name | Position Importance |
|---------|-----------|-----------|---------------------|
| `PSPD` | `PSDX` | Speed | All |
| `PAGI` | `PAGX` | Agility | RB, WR, DB |
| `PACC` | `PACX` | Acceleration | RB, WR, DB |
| `PSTR` | `PSTX` | Strength | OL, DL, LB |
| `PAWR` | `PAWX` | Awareness | All |
| `PSTA` | `PSAX` | Stamina | All |
| `PINJ` | `PINX` | Injury | All |
| `PLRN` | `PLRX` | Learning | All (min 75 recommended) |

### Position-Specific Stats

#### Passing (QB)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PTHA` | `PTAX` | Throw Accuracy |
| `PTHP` | `PTPX` | Throw Power |

#### Rushing/Receiving (RB, WR, TE)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PCAR` | `PCAX` | Carrying |
| `PELU` | `PELX` | Elusiveness |
| `PBCV` | `PBCX` | Ball Carrier Vision |

#### Catching (WR, TE, RB)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PCTH` | `PCTX` | Catching |
| `PLSC` | `PSCX` | Short Catch |
| `PLCI` | `PLCX` | Catch In Traffic |
| `PLRR` | `PRRX` | Route Running (Right) |
| `PLRL` | `PRLX` | Route Running (Left) |

#### Blocking (OL, TE, FB)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PPBK` | `PPBX` | Pass Block |
| `PRBK` | `PRBX` | Run Block |
| `PLIB` | `PIBX` | Lead Block |
| `PRBS` | `PRSX` | Run Block Strength |
| `PRBF` | `PRFX` | Run Block Footwork |
| `PPBS` | `PPSX` | Pass Block Strength |
| `PPBF` | `PPFX` | Pass Block Footwork |

#### Defense (DL, LB, DB)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PTAK` | `PTKX` | Tackling |
| `PLHT` | `PLHX` | Hit Power |
| `PLPm` | `PPMX` | Play Recognition |
| `PFMS` | `PFMX` | Man Coverage |
| `PBSG` | `PBSX` | Zone Coverage |
| `PLPU` | `PPUX` | Pursuit |
| `PLPR` | `PPRX` | Press Coverage |

#### Special Teams (K, P)

| Current | Potential | Stat Name |
|---------|-----------|-----------|
| `PKPR` | `PKPX` | Kick Power |
| `PKAC` | `PKAX` | Kick Accuracy |
| `PKRT` | `PKRX` | Kick Return |

### Health/Injury Fields

| Field | Description | Range | Notes |
|-------|-------------|-------|-------|
| `PLAC` | Left Ankle/Foot Condition | 0-1000 | Higher = healthier |
| `PRAC` | Right Ankle/Foot Condition | 0-1000 | |
| `PHDC` | Head Condition | 0-1000 | |
| `PLLC` | Left Leg Condition | 0-1000 | |
| `PTRC` | Torso Condition | 0-1000 | |
| `PRLc` | Right Leg Condition | 0-1000 | |
| `PTGH` | Toughness | 0-99 | Injury resistance |
| `PINJ` | Injury Rating | 0-99 | Lower = more durable |

### Contract Fields

| Field | Description | Range | Notes |
|-------|-------------|-------|-------|
| `PSA0`-`PSA6` | Salary by Year | 0-999 | In $10,000s (24 = $240K) |
| `PSB0`-`PSB6` | Bonus by Year | 0-999 | In $10,000s |
| `PCSA` | Current Salary | 0-999 | Current year salary |
| `PTSA` | Total Salary | 0-9999 | Sum of all years |
| `PVSB` | Veteran Signing Bonus | 0-999 | |
| `PCYL` | Contract Years Left | 0-7 | |
| `PCON` | Contract Length | 0-7 | Original length |
| `PSBO` | Signing Bonus | 0-999 | |
| `PVCO` | Void Clause | 0-1 | Boolean |
| `PFHO` | Franchise Tag | 0-1 | Boolean |

### Personality/Traits

| Field | Description | Range | Notes |
|-------|-------------|-------|-------|
| `PTId` | Personality Trait ID | 0-15 | 9 = Captain (recommended) |

### Advanced/Miscellaneous

| Field | Description | Notes |
|-------|-------------|-------|
| `SKPT` | Skill Points | 0-131000 (max) |
| `PLSA` | Long Snap (LS position) | |
| `PLSM` | Long Snap Medium | |
| `PLJM` | Long Jump | |
| `PJMP` | Jump | Vertical leap |
| `PLMC` | Man Coverage (slot) | |
| `PLZC` | Zone Coverage (slot) | |
| `PLPE` | Press Coverage (slot) | |

## Coach Fields

### Identity Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `CFNM` | First Name | "Bill" |
| `CLNM` | Last Name | "Belichick" |
| `COPS` | Position Code | 0-10 (see Coach Positions) |
| `TGID` | Team ID | 1-33 |
| `PNid` | Personnel ID | Unique identifier |

### General Coaching Stats

| Field | Description | Range |
|-------|-------------|-------|
| `SKPA` | Play Calling Ability | 0-5 |
| `SKCM` | Clock Management | 0-5 |
| `SKSM` | Staff Management | 0-5 |
| `SKPX` | Potential (max of above) | 0-5 |

### Positional Coaching (in cskl.csv)

| Field | Description | Range |
|-------|-------------|-------|
| `SKIM` | Individual Motivation | 0-5 |
| `SKPM` | Position Motivation | 0-5 |
| `SKLM` | Leadership/Management | 0-5 |

### Common Fields

| Field | Description | Range |
|-------|-------------|-------|
| `SKPT` | Skill Points | 0-131000 |
| `PTId` | Personality | 0-15 (9 = Captain) |

## GM Fields

### Identity Fields

| Field | Description |
|-------|-------------|
| `TGID` | Team ID |
| `PNid` | Personnel ID |

### General GM Stats

| Field | Description | Range |
|-------|-------------|-------|
| `SKTM` | Trade Management | 0-5 |
| `SKTD` | Trade Decisions | 0-5 |
| `SKNM` | Negotiation Management | 0-5 |
| `SKNG` | Negotiation General | 0-5 |

### Positional GM Skills (in gmsk.csv)

| Field | Description | Range |
|-------|-------------|-------|
| `SKRM` | Roster Management | 0-5 |
| `SKSX` | Scouting | 0-5 |

### Common Fields

| Field | Description | Range |
|-------|-------------|-------|
| `SKPT` | Skill Points | 0-131000 |
| `PTId` | Personality | 0-15 |

## Trainer Fields

### Identity Fields

| Field | Description |
|-------|-------------|
| `TGID` | Team ID |
| `PNid` | Personnel ID |

### Trainer Stats

| Field | Description | Range |
|-------|-------------|-------|
| `TSIM` | Injury Management | 0-5 |
| `TSRM` | Rehabilitation Management | 0-5 |
| `TSFM` | Fitness Management | 0-5 |

### Common Fields

| Field | Description | Range |
|-------|-------------|-------|
| `SKPT` | Skill Points | 0-131000 |
| `PTId` | Personality | 0-15 |

## Reference Tables

### Position Codes (PPOS)

| Code | Position | Code | Position |
|------|----------|------|----------|
| 0 | QB | 11 | RE |
| 1 | HB | 12 | DT |
| 2 | FB | 13 | LOLB |
| 3 | WR | 14 | MLB |
| 4 | TE | 15 | ROLB |
| 5 | LT | 16 | CB |
| 6 | LG | 17 | FS |
| 7 | C | 18 | SS |
| 8 | RG | 19 | K |
| 9 | RT | 20 | P |
| 10 | LE | - | - |

### Coach Position Codes (COPS)

| Code | Position |
|------|----------|
| 0 | Head Coach (HC) |
| 1 | Offensive Coordinator (OC) |
| 2 | Defensive Coordinator (DC) |
| 3 | Special Teams Coordinator (STC) |
| 4 | Quarterbacks Coach (QBC) |
| 5 | Running Backs Coach (RBC) |
| 6 | Wide Receivers Coach (WRC) |
| 7 | Offensive Line Coach (OLC) |
| 8 | Defensive Line Coach (DLC) |
| 9 | Linebackers Coach (LBC) |
| 10 | Defensive Backs Coach (DBC) |

### Team IDs (TGID)

See [Usage Guide - Team ID Reference](../guides/usage.md#team-id-reference) for complete list.

**Special:**
- **33:** Free Agents / Unassigned

## Best Practices

### Safe Value Ranges

When manually editing fields:

| Field Type | Safe Range | Notes |
|------------|------------|-------|
| Player stats | 0-99 | Current and potential |
| Health stats | 0-1000 | Condition fields |
| Coach stats | 0-5 | All coaching attributes |
| Age | 21-40 | Outside range may cause issues |
| Contract years | 0-7 | NFL max contract length |
| Salary | 24-999 | League min = 24 ($240K) |
| Height | 65-85 | Inches (5'5" to 7'1") |
| Weight | 160-380 | Pounds |

### Validation Tips

1. **Stay within ranges:** Exceeding maximums can corrupt data
2. **Match data types:** Don't put text in numeric fields
3. **Preserve ID fields:** Never modify `PNid` or unique identifiers
4. **Test incrementally:** Change one field, import, verify
5. **Reference vanilla rosters:** Check original export for valid value examples

## Advanced Editing

### Creating Custom Fields

**Not supported.** HC09 expects specific field structure. Adding fields will likely cause import failures.

### Deleting Fields

**Not recommended.** Missing expected fields may crash game or cause corruption.

### Multi-Field Dependencies

Some fields affect each other:

- **Contract:** Changing `PCYL` should match total salary fields
- **Stats:** Current should never exceed potential
- **Health:** Multiple injury fields work together

## Troubleshooting Field Changes

If custom changes cause issues:

1. **Verify field name:** Exactly 4 characters, case-sensitive
2. **Check value type:** Numeric fields need numbers
3. **Confirm range:** Stay within safe ranges
4. **Test in vanilla:** Try same change on fresh export
5. **Isolate change:** Modify one field at a time

## Further Reading

- [Usage Guide](../guides/usage.md) - Standard operations that safely modify fields
- [Troubleshooting](../guides/troubleshooting.md) - Error resolution
- [Quick Start](../getting-started/quickstart.md) - Safe operations for beginners
