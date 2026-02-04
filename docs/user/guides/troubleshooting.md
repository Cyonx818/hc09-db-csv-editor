---
audience: user
---

# Troubleshooting Guide

> **Purpose:** Solutions to common issues when using the NFL Head Coach '09 CSV Editor.
> **Audience:** All users encountering problems with the tool.

## Common Issues

### File Not Found Errors

#### Symptom
```
File not found. Please try again.
```

#### Causes & Solutions

**Wrong file path:**
- Check spelling and capitalization
- Use full absolute path: `C:\HC09\exports\players.csv`
- On Windows, use backslashes (`\`) or forward slashes (`/`)
- Avoid spaces in paths or use quotes: `"C:\My Files\roster.csv"`

**File doesn't exist:**
- Verify file exists: Run `dir` (Windows) or `ls` (macOS/Linux) in the directory
- Ensure CSV was exported successfully from your save editor

**Wrong directory:**
- Navigate to the directory containing the CSV before running tool
- Or provide full path to CSV file

### Roster Type Detection Failures

#### Symptom
```
Unknown roster type
```

#### Cause
CSV file is not a valid HC09 roster export.

#### Solutions

1. **Verify export format:** Ensure CSV exported from valid HC09 save editor
2. **Check headers:** Open CSV in text editor - first line should start with:
   - `PSA0` (Players)
   - `CFDA` (Coaches)
   - `GMAB` (GMs)
   - `TRAB` (Trainers)
3. **Re-export:** Try exporting roster again from save editor
4. **Check encoding:** File should be UTF-8 encoded

### Player/Coach Not Found

#### Symptom
```
Player not found. Please try again.
```

#### Causes & Solutions

**Name typo:**
- Verify exact spelling by using "List all Players on a team" first
- Names are case-sensitive but input matching is case-insensitive

**Wrong roster file:**
- Ensure you're searching in the correct roster type (can't find players in coach roster)

**Player on different team:**
- Check free agents (Team ID 33)
- List all teams to find player's current team

### Companion File Warnings

#### Symptom
```
cskl.csv not found. Editing positional stats is impossible!
```

#### Cause
Trying to edit positional coach skills without `cskl.csv` (or `gmsk.csv` for GMs).

#### Solutions

1. **Export companion file:** Use save editor to export positional skill file
2. **Place in same directory:** Put `cskl.csv` in same folder as coach roster CSV
3. **Skip positional operations:** Use only general coaching operations
4. **Check filename:** Must be exactly `cskl.csv` or `gmsk.csv` (case-insensitive)

### Changes Not Saved

#### Symptom
Modified CSV file not created or changes not reflected in-game.

#### Causes & Solutions

**Chose "no" when prompted:**
- Re-run tool and select "yes" when asked to save

**File permission issues:**
- Ensure output directory is writable
- Try running from a different directory
- Check disk space

**Modified file overwritten:**
- Tool creates `_modified.csv` or `_modified_1.csv`, `_modified_2.csv`, etc.
- Check for incrementing numbers if you've saved multiple times

**Import failed:**
- Verify you imported the `_modified.csv` file, not the original
- Check save editor import process for errors
- Ensure modified CSV format matches game expectations

### Invalid Key Errors

#### Symptom
```
Key 'XXXX' not found in member data. Please try again.
```

#### Cause
Using "Change Key Value" with a non-existent field name.

#### Solutions

1. **Check field reference:** See [CSV Fields Reference](../reference/csv-fields.md)
2. **Verify case:** Keys are case-sensitive (`PSPD` not `pspd`)
3. **Confirm length:** Must be exactly 4 characters
4. **Roster type specific:** Some keys only exist in certain roster types

### CSV Corruption After Editing

#### Symptom
Modified CSV can't be imported or causes game crashes.

#### Causes & Solutions

**Invalid value entered:**
- Ensure values are within valid ranges:
  - Player stats: 0-99 (or 0-1000 for health)
  - Coach stats: 0-5
  - Contract years: 0-7
  - Age: 21-40 recommended

**Non-numeric value in numeric field:**
- Don't enter text in stat fields
- Tool doesn't validate custom key changes

**Encoding issues:**
- If CSV looks garbled, may be encoding problem
- Re-export from save editor with UTF-8 encoding

#### Recovery

1. Delete corrupted CSV
2. Use backup or re-export from save
3. Make changes more conservatively
4. Test import after each major edit

## Platform-Specific Issues

### Windows

**Backslash escaping:**
```bash
# Wrong
python hc09-db-csv-editor.py C:\HC09\roster.csv

# Right
python hc09-db-csv-editor.py "C:\HC09\roster.csv"
# or
python hc09-db-csv-editor.py C:/HC09/roster.csv
```

**Python not in PATH:**
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python39\python.exe hc09-db-csv-editor.py`

### macOS/Linux

**Python 2 vs Python 3:**
```bash
# If 'python' is Python 2.x, use:
python3 hc09-db-csv-editor.py roster.csv
```

**Permission denied:**
```bash
chmod +x hc09-db-csv-editor.py
./hc09-db-csv-editor.py roster.csv
```

**Line ending issues:**
- If CSV exported on Windows, may have CRLF line endings
- Usually handled automatically, but if errors occur:
```bash
dos2unix roster.csv  # Convert CRLF to LF
```

## Advanced Troubleshooting

### Debugging Invalid Values

If uncertain what value to use for a field:

1. Edit one player with known stats
2. Export to CSV
3. Open in text editor or spreadsheet
4. Find player's row
5. Note value format for each field
6. Use same format in tool

### Comparing Before/After

To verify changes:

```bash
# On Unix systems
diff original.csv original_modified.csv

# On Windows PowerShell
Compare-Object (Get-Content original.csv) (Get-Content original_modified.csv)
```

### Manual CSV Editing

If tool doesn't support needed operation:

1. Open `_modified.csv` in spreadsheet software (Excel, LibreOffice)
2. Find player row
3. Edit cells directly
4. Save as CSV (UTF-8 encoding)
5. Import to game

**Warning:** Manual editing can corrupt CSV if format violated.

## Error Messages Reference

| Message | Meaning | Solution |
|---------|---------|----------|
| `File not found` | CSV path invalid | Check path and filename |
| `Unknown roster type` | Invalid roster CSV | Verify export from HC09 |
| `Player not found` | Name search failed | Check spelling, try team list |
| `Stat ... does not exist` | Invalid field key | Use 4-char field name from reference |
| `cskl.csv not found` | Missing companion file | Export cskl.csv from save |
| `Invalid team ID` | Team number not 1-33 | Use team list for valid IDs |
| `Invalid key name. It must be a 4-character string` | Key wrong length | Enter exactly 4 characters |

## Still Having Issues?

If your problem isn't covered here:

1. **Check documentation:**
   - [Installation Guide](../getting-started/installation.md)
   - [Quick Start](../getting-started/quickstart.md)
   - [Usage Guide](usage.md)

2. **Create minimal test case:**
   - Export fresh CSV from save editor
   - Test with single simple operation
   - Isolate where failure occurs

3. **Report the issue:**
   - GitHub Issues: Include error message, roster type, operation attempted
   - Provide steps to reproduce
   - Attach sample CSV if possible (sanitize personal data)

## Prevention Tips

1. **Always backup:** Keep original CSV before editing
2. **Test incrementally:** Make small changes, test import, repeat
3. **Use standard operations:** Custom key changes are risky
4. **Verify file paths:** Copy/paste paths to avoid typos
5. **Check companion files:** Ensure cskl.csv/gmsk.csv present if needed
