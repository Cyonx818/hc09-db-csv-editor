import csv
import os
import argparse

# Constants
MAXPLAYERSTAT = 99
MAXHEALTH = 1000
MAXSKILLPOINTS = 131000
MAXCOACHSTAT = 5
MAXGMSTAT = MAXCOACHSTAT
MINPLRN = 75
TEAM_NAMES = {
        "1": "Bears (Chicago)",
        "2": "Bengals (Cincinnati)",
        "3": "Bills (Buffalo)",
        "4": "Broncos (Denver)",
        "5": "Browns (Cleveland)",
        "6": "Buccaneers (Tampa Bay)",
        "7": "Cardinals (Arizona)",
        "8": "Chargers (Los Angeles)",
        "9": "Chiefs (Kansas City)",
        "10": "Colts (Indianapolis)",
        "11": "Cowboys (Dallas)",
        "12": "Dolphins (Miami)",
        "13": "Eagles (Philadelphia)",
        "14": "Falcons (Atlanta)",
        "15": "49ers (San Francisco)",
        "16": "Giants (New York)",
        "17": "Jaguars (Jacksonville)",
        "18": "Jets (New York)",
        "19": "Lions (Detroit)",
        "20": "Packers (Green Bay)",
        "21": "Panthers (Carolina)",
        "22": "Patriots (New England)",
        "23": "Raiders (Las Vegas)",
        "24": "Rams (Los Angeles)",
        "25": "Ravens (Baltimore)",
        "26": "Redskins (Washington)",
        "27": "Saints (New Orleans)",
        "28": "Seahawks (Seattle)",
        "29": "Steelers (Pittsburgh)",
        "30": "Texans (Houston)",
        "31": "Titans (Tennessee)",
        "32": "Vikings (Minnesota)",
        "33": "Free Agents",
    }


# Global Variables
skill_members = None
changes = False


# Class definitions
class Member:
    def __init__(self, data):
        self.data = data

    def set_stat(self, stat_key, value):
        if stat_key in self.data:
            self.data[stat_key] = value
        else:
            print(f"Stat {stat_key} does not exist.")

        
# IO & UI Functions
def get_input_file():
    parser = argparse.ArgumentParser(description="Process player roster CSV.")
    parser.add_argument('input_file', nargs='?', help="Path to the input CSV file.")
    args = parser.parse_args()

    if args.input_file and os.path.isfile(args.input_file):
        return args.input_file
    else:
        while True:
            input_file = input("Enter the path to the input CSV file: ").strip()
            if os.path.isfile(input_file):
                return input_file
            else:
                print("File not found. Please try again.")            


def main_menu(roster_type, members, headers, input_csv_path):
    member_index = None
    skill_file = None
    global skill_members
    if (roster_type == "Coach") or (roster_type == "GM"):
        skill_file = find_skill_file(input_csv_path, roster_type)
        skill_headers, skill_members = read_members_from_csv(skill_file)
    while True:
        if (roster_type == 'Player') or (roster_type == 'Coach'):
            print("\nMain Menu:")
            print(f"1. List all {roster_type}s on a team")
            print(f"2. Select a {roster_type} by name")
            print("q. Quit")

            choice = input("Enter your choice: ").strip().lower()

            if choice == '1':
                list_roster_by_team(roster_type, members)
            elif choice == '2':
                while True:
                    first_name = input("Enter member's first name (or 'q' to quit): ").strip()
                    if first_name.lower() in ['q', 'quit']:
                        break
                    last_name = input("Enter member's last name (or 'q' to quit): ").strip()
                    if last_name.lower() in ['q', 'quit']:
                        break
                    member_index = find_member_index(members, first_name, last_name, roster_type)

                    if member_index is not None:
                        modify_roster_member(roster_type, members[member_index])
                        break
                    else:
                        print(f"{roster_type} not found. Please try again.")
            elif choice in ['q', 'quit']:
                break
            else:
                print("Invalid choice. Please try again.")
        elif(roster_type == 'GM') or (roster_type == 'Trainer'):
            print("\nMain Menu:")
            print(f"1. Select a {roster_type} by team")
            print("q. Quit")

            choice = input("Enter your choice: ").strip().lower()

            if choice == '1':
                find_member_by_team(members, roster_type)
            elif choice in ['q', 'quit']:
                break
            else:
                print("Invalid choice. Please try again.")
    if changes:
        save_changes_confirmation(members, headers, input_csv_path)
        if skill_file:
            save_changes_confirmation(skill_members, skill_headers, skill_file)


def read_members_from_csv(file_path):
    headers = []
    members = []
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        for row in reader:
            members.append(Member(row))
    return headers, members


def save_changes_confirmation(members, headers, input_csv_path):
    while True:
        save_changes = input(f"Do you want to save changes to {input_csv_path}? (yes/no): ").strip().lower()
        if save_changes in ['y', 'yes']:
            write_members_to_csv(members, headers, input_csv_path)
            break
        elif save_changes in ['n', 'no']:
            print("Changes not saved.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def write_members_to_csv(members, headers, input_file):
    base, ext = os.path.splitext(input_file)
    output_file = base + "_modified" + ext
    count = 1
    while os.path.exists(output_file):
        output_file = f"{base}_modified_{count}{ext}"
        count += 1
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for member in members:
            writer.writerow(member.data)
    print(f"Changes saved to {output_file}")


# Universal Roster Functions
def captain_personality(member):
    member.set_stat("PTId", 9)


def change_key_value(member):
    while True:
        key = input("Enter key name to change (4-character Case Sensitive): ").strip()
        if len(key) != 4:
            print("Invalid key name. It must be a 4-character string.")
            continue
        if key in member.data:
            print(f"Current value for {key}: {member.data[key]}")
            new_value = input(f"Enter new value for {key}: ").strip()
            member.set_stat(key, new_value)
            break
        else:
            print(f"Key '{key}' not found in member data. Please try again.")


def detect_roster_type(headers):
    if headers[0] == "PSA0":
        return "Player"
    elif headers[0] == "CFDA":
        return "Coach"
    elif headers[0] == "TRAB":
        return "Trainer"
    elif headers[0] == "GMAB":
        return "GM"
    else:
        raise ValueError("Unknown roster type")


def find_member_by_team(members, roster_type):
    print(f"Which team's {roster_type} do you want to edit?")
    print_team_names()
    team_id = input("\nEnter team ID (1-33): ").strip()

    if team_id == "33":
        team_members = [member for member in members if member.data['TGID'] not in map(str, range(1, 33))]
    elif team_id in TEAM_NAMES:
        team_members = [member for member in members if member.data['TGID'] == team_id]
    else:
        print(f"Invalid team ID: {team_id}")
        return None
    
    if not team_members:
        print(f"No {roster_type} found for team ID {team_id}.")
        return None
    else:
        member = team_members[0]
        if roster_type == 'Trainer':
            modify_trainer(member)
        elif roster_type == 'GM':
            modify_gm(member)


def find_member_index(members, first_name, last_name, roster_type):
    name_keys = {
        "Player": ("PFNA", "PLNA"),
        "Coach": ("CFNM", "CLNM"),
        "GM": None,  # GMs do not have editable names
        "Trainer": None  # Trainers do not have editable names
    }
    
    if roster_type in name_keys and name_keys[roster_type] is not None:
        first_name_key, last_name_key = name_keys[roster_type]
        for i, member in enumerate(members):
            if (member.data[first_name_key].lower() == first_name.lower() and 
                member.data[last_name_key].lower() == last_name.lower()):
                return i
    return None


def find_skill_file(filepath, roster_type):
    directory = os.path.dirname(filepath)
    if roster_type == "Coach":
        target_file = "cskl.csv"
    if roster_type == "GM":
        target_file = "gmsk.csv"
    filefound = None
    for filename in os.listdir(directory):
        if filename.lower() == target_file.lower():
            filefound = os.path.join(directory, filename)
            print(f"{target_file} found at {filefound}!")
    if not filefound:
        print(f"{target_file} not found. Editing positional stats is impossible!")
    return filefound  


def list_roster_by_team(roster_type, members):
    if roster_type == "Player":
        list_players_by_team(members)
    elif roster_type == "Coach":
        list_coaches_by_team(members)
    # GMs and Trainers do not use this step


def modify_member(actions, member, roster_type):
    global skill_members
    global changes
    member_type = roster_type.lower()
    if member_type == "gm":
        member_type = "GM"
    while True:
        print("Choose an action to perform:")
        for key, (description, _) in actions.items():
            print(f"{key}. {description}")
        print(f"q. Quit to {member_type} selection")

        choice = input("Enter the number of your choice: ").strip().lower()
        if choice in actions:
            _, action = actions[choice]
            action(member)
            changes = True
            print(f"Action '{actions[choice][0]}' performed on {member_type}.")
        elif choice in ['q', 'quit']:
            break
        else:
            print("Invalid choice. Please try again.")


def modify_roster_member(roster_type, member):
    if roster_type == 'Player':
        modify_player(member)
    elif roster_type == 'Coach':
        modify_coach(member)
    # GMs and Trainers do not use this step


def practice_really_hard(member):
    member.set_stat('SKPT', MAXSKILLPOINTS)


def print_team_names():
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


# Player specific functions
def list_players_by_team(players):
    position_abbr = {
        "0": "QB",
        "1": "HB",
        "2": "FB",
        "3": "WR",
        "4": "TE",
        "5": "LT",
        "6": "LG",
        "7": "C",
        "8": "RG",
        "9": "RT",
        "10": "LE",
        "11": "RE",
        "12": "DT",
        "13": "LOLB",
        "14": "MLB",
        "15": "ROLB",
        "16": "CB",
        "17": "FS",
        "18": "SS",
        "19": "K",
        "20": "P"
    }

    print_team_names()

    team_id = input("\nEnter team ID (1-33): ").strip()

    if team_id == "33":
        team_players = [player for player in players if player.data['TGID'] not in map(str, range(1, 33))]
    elif team_id in TEAM_NAMES:
        team_players = [player for player in players if player.data['TGID'] == team_id]
    else:
        print(f"Invalid team ID: {team_id}")
        return

    if team_players:
        print("\nPlayer List:")
        line = ""
        for i, player in enumerate(team_players):
            pos_num = player.data['PPOS']
            position = position_abbr.get(pos_num, "Unknown")
            first_name = player.data['PFNA']
            last_name = player.data['PLNA']
            display_str = f"{position} {first_name} {last_name}"
            if len(line) + len(display_str) > 80:
                print(line)
                line = ""
            line += f"{display_str:<25}\t"
        print(line)
    else:
        print(f"No players found for team ID {team_id}.")


def max_health(player):
    health_keys = ['PLAC', 'PRAC', 'PHDC', 'PLLC', 'PTRC', 'PRLc', 'PSTA', 'PTGH', 'PINJ']
    for key in health_keys:
        if key in player.data:
            current_value = int(player.data[key])
            if current_value > MAXPLAYERSTAT:
                new_value = MAXHEALTH
            else:
                new_value = MAXPLAYERSTAT
            player.set_stat(key, new_value)
    if int(player.data['PLRN']) < MINPLRN:
        player.set_stat('PLRN', MINPLRN)


def max_potential(player):
    for key in player.data:
        if key.endswith('x') or key.endswith('X'):
            current_value = int(player.data[key])
            if current_value > MAXPLAYERSTAT:
                new_value = MAXHEALTH
            else:
                new_value = MAXPLAYERSTAT
            player.set_stat(key, new_value)


def make_physical_specimen(player):
    player.set_stat('PAGE', 21)

    current_height = player.data.get('PHGT', 0)
    current_weight = player.data.get('PWGT', 0)

    new_height = int(float(current_height) * 1.1)
    new_weight = int(float(current_weight) * 1.1)

    player.set_stat('PHGT', new_height)
    player.set_stat('PWGT', new_weight)


def modify_player(player):
    actions = {
        "1": ("Maximize Potential", max_potential),
        "2": ("Maximize Health", max_health),
        "3": ("Resign for Peanuts", resign_for_peanuts),
        "4": ("Make Physical Specimen", make_physical_specimen),
        "5": ("Rename Player", rename_player),
        "6": ("Change Key Value", change_key_value),
    }

    modify_member(actions, player, "Player")


def rename_player(player):
    first_name = input("Enter new first name (case-sensitive): ").strip()
    last_name = input("Enter new last name (case-sensitive): ").strip()
    player.set_stat('PFNA', first_name)
    player.set_stat('PLNA', last_name)


def resign_for_peanuts(player):
    salary_key_value_dict = {
        'PSA0': 24,
        'PSA1': 24,
        'PSA2': 24,
        'PSA3': 24,
        'PSA4': 24,
        'PSA5': 24,
        'PSA6': 24,
        'PSB0': 0,
        'PSB1': 0,
        'PSB2': 0,
        'PSB3': 0,
        'PSB4': 0,
        'PSB5': 0,
        'PSB6': 0,
        'PCSA': 24,
        'PTSA': 168,
        'PVSB': 0,
        'PCYL': 7,
        'PCON': 7,
        'PSBO': 0,
        'PVCO': 0,
        'PFHO': 0,
        'PTId': 9,
    }
    for key, new_value in salary_key_value_dict.items():
        if key in player.data:
            player.set_stat(key, new_value)


# Coach specific functions  
def list_coaches_by_team(coaches):
    position_abbr = {
        "0": "HC",
        "1": "OC",
        "2": "DC",
        "3": "STC",
        "4": "QBC",
        "5": "RBC",
        "6": "WRC",
        "7": "OLC",
        "8": "DLC",
        "9": "LBC",
        "10": "DBC",
    }

    print_team_names()

    team_id = input("\nEnter team ID (1-33): ").strip()

    if team_id == "33":
        team_coaches = [coach for coach in coaches if coach.data['TGID'] not in map(str, range(1, 33))]
    elif team_id in TEAM_NAMES:
        team_coaches = [coach for coach in coaches if coach.data['TGID'] == team_id]
    else:
        print(f"Invalid team ID: {team_id}")
        return

    if team_coaches:
        print("\nCoach List:")
        line = ""
        for i, coach in enumerate(team_coaches):
            pos_num = coach.data['COPS']
            position = position_abbr.get(pos_num, "Unknown")
            first_name = coach.data['CFNM']
            last_name = coach.data['CLNM']
            display_str = f"{position} {first_name} {last_name}"
            if len(line) + len(display_str) > 80:
                print(line)
                line = ""
            line += f"{display_str:<25}\t"
        print(line)
    else:
        print(f"No coaches found for team ID {team_id}.")


def max_general_coaching_potential(coach):
    keys = ['SKPA', 'SKCM', 'SKSM', 'SKPX']
    for key in keys:
        coach.set_stat(key, MAXCOACHSTAT)


def max_positional_coaching_potential(coach):
    global skill_members
    keys = ["SKIM", "SKPM", "SKLM"] 
    if skill_members:
        for member in skill_members:
            if member.data["PNid"] == coach.data["PNid"]:
                for key in keys:
                    member.set_stat(key, MAXCOACHSTAT)
    else:
        print("Warning: No CSKL file found. Coach Positional editing not possible")
    pass


def modify_coach(coach):
    actions = {
        "1": ("Max General Coaching Potential", max_general_coaching_potential),
        "2": ("Max Positional Coaching Potential", max_positional_coaching_potential),
        "3": ("Practice Really Hard (Max Skill Points)", practice_really_hard),
        "4": ("Take old boy out for drinks (Captain personality)", captain_personality),
        "5": ("Rename Coach", rename_coach),
        "6": ("Change Key Value", change_key_value),
    }

    modify_member(actions, coach, "Coach")


def rename_coach(coach):
    first_name = input("Enter new first name (case-sensitive): ").strip()
    last_name = input("Enter new last name (case-sensitive): ").strip()
    coach.data['CFNM'] = first_name
    coach.data['CLNM'] = last_name


# GM specific functions
def max_general_gm_potential(gm):
    keys = ['SKTM', 'SKTD', 'SKNM', 'SKNG']
    for key in keys:
        gm.set_stat(key, MAXGMSTAT)


def max_positional_gm_potential(gm):
    global skill_members
    keys = ["SKRM", "SKSX"] 
    if skill_members:
        for member in skill_members:
            if member.data["PNid"] == gm.data["PNid"]:
                for key in keys:
                    member.set_stat(key, MAXGMSTAT)
    else:
        print("Warning: No GMSK file found. GM Positional editing not possible.")
    pass


def modify_gm(gm):
    actions = {
        "1": ("Max General GM Potential", max_general_gm_potential),
        "2": ("Max Positional GM Potential", max_positional_gm_potential),
        "3": ("Practice Really Hard (Max Skill Points)", practice_really_hard),
        "4": ("Take old boy out for drinks (Captain personality)", captain_personality),
        # "5": ("Rename GM", rename_gm),
        "5": ("Change Key Value", change_key_value),
    }
    modify_member(actions, gm, 'GM')

def rename_gm(gm):
    pass # requires PERV file to be dumped in order to implement.


# Trainer specific functions
def max_trainer_potential(trainer):
    keys = ['TSIM', 'TSRM', 'TSFM']
    for key in keys:
        trainer.set_stat(key, MAXGMSTAT)


def modify_trainer(trainer):
    actions = actions = {
        "1": ("Max Trainer Potential", max_trainer_potential),
        "2": ("Practice Really Hard (Max Skill Points)", practice_really_hard),
        "3": ("Take old boy out for drinks (Captain personality)", captain_personality),
        # "5": ("Rename Trainer", rename_trainer),
        "4": ("Change Key Value", change_key_value),
    }
    modify_member(actions, trainer, 'Trainer')


def rename_trainer(trainer):
    pass # requires PERV file to be dumped in order to implement.


# main()
def main():
    input_csv_path = get_input_file()

    headers, members = read_members_from_csv(input_csv_path)
    roster_type = detect_roster_type(headers)
    print(f"Detected roster type: {roster_type}")

    main_menu(roster_type, members, headers, input_csv_path)

if __name__ == "__main__":
    main()
