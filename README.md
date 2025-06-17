# hc09-db-csv-editor

A command-line tool for bulk editing attributes in CSV exports from NFL Head Coach '09 save games and roster databases. This script streamlines mass updates to players, coaches, GMs, and trainers, making roster management and customization much easier.

## Features
- Bulk edit player, coach, GM, and trainer attributes
- Randomize names for players and coaches
- Maximize stats, skill points, and potentials
- Change key values for any member
- CSV import/export for seamless integration with HC09 Editor

## Requirements
- Python 3.7 or newer
- [HC09 Editor v1.3.2+](https://github.com/your-hc09-editor-link) (for exporting/importing CSVs)

## Installation
1. Clone this repository or download the script:
   ```sh
   git clone https://github.com/yourusername/hc09-db-csv-editor.git
   cd hc09-db-csv-editor
   ```
2. (Optional) Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install any required dependencies (none for standard library usage).

## Preparing Your CSV Files
1. Open your savegame in HC09 Editor (use the DB editor, **not** 'Load Career File' or 'Edit Game Files').
2. Export the following databases to CSV files, using these exact names:
   - `play.csv` (Players)
   - `coch.csv` (Coaches)
   - `gmvw.csv` (GMs)
   - `trvw.csv` (Trainers)
   - `cskl.csv` (Coach Skills)
   - `gmsk.csv` (GM Skills)

## Usage
Run the script from the command line, specifying the path to your target CSV file:

```sh
python3 hc09-db-csv-editor.py play.csv
```

If you do not provide a file, the script will prompt you for the path.

### Interactive Menu
The script will detect the roster type and present an interactive menu for bulk editing, randomizing names, or modifying individual members.

#### Example Workflow
1. List all players or coaches on a team
2. Select a member by name for editing
3. Bulk edit all members of a team
4. Randomize names (affects all members of the selected type)
5. Save your changes and re-import the CSV into HC09 Editor

## Saving Changes
After editing, import the modified CSV back into the DB editor, overwrite the original DB, and save your modified savegame.

## Contributing
Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

## License
[MIT License](LICENSE)  
Copyright (c) Pat Swanson

## Support
For questions or help, open an issue on this repository.
