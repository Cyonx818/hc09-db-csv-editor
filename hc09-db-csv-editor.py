import csv
import os
import argparse
import random


# Constants
MAXPLAYERSTAT = 99
MAXHEALTH = 1000
MAXSKILLPOINTS = 131000
MAXCOACHSTAT = 5
MAXGMSTAT = MAXCOACHSTAT
MINPLRN = 75
PLAYER_FIRST_NAME_CODE = 'PFNA'
PLAYER_LAST_NAME_CODE = 'PLNA'
COACH_FIRST_NAME_CODE = 'CFNM'
COACH_LAST_NAME_CODE = 'CLNM'
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
PLAYER_STATS = {
    'PSPD': 'PSDX',
    'PAGI': 'PAGX',
    'PACC': 'PACX',
    'PSTR': 'PSTX',
    'PAWR': 'PAWX',
    'PSTA': 'PSAX',
    'PINJ': 'PINX',
    'PLTR': 'PLTX',
    'PELU': 'PELX',
    'PBCV': 'PBCX',
    'PLSA': 'PLSX',
    'PLSM': 'PSMx',
    'PLJM': 'PLJX',
    'PCAR': 'PCAX',
    'PTHP': 'PTPX',
    'PTHA': 'PTAX',
    'PCTH': 'PCTX',
    'PLSC': 'PSCX',
    'PLCI': 'PLCX',
    'PLRR': 'PRRX',
    'PLRL': 'PRLX',
    'PJMP': 'PJMX',
    'PPBK': 'PPBX',
    'PRBK': 'PRBX',
    'PLIB': 'PIBX',
    'PRBS': 'PRSX',
    'PRBF': 'PRFX',
    'PPBS': 'PPSX',
    'PPBF': 'PPFX',
    'PTAK': 'PTKX',
    'PLHT': 'PLHX',
    'PLPm': 'PPMX',
    'PFMS': 'PFMX',
    'PBSG': 'PBSX',
    'PLPU': 'PPUX',
    'PLPR': 'PPRX',
    'PLMC': 'PLMX',
    'PLZC': 'PLZX',
    'PLPE': 'PPEX',
    'PKPR': 'PKPX',
    'PKAC': 'PKAX',
    'PKRT': 'PKRX',
    'PLRN': 'PLRX',
    'PTGH': 'PTGX'
}


# Global Variables
skill_members = None
changes = False
roster_type = ''


# Class definitions
class Member:
    global roster_type
    def __init__(self, data):
        self.data = data

    def set_stat(self, stat_key, value):
        if stat_key in self.data:
            self.data[stat_key] = value
        else:
            print(f"Stat {stat_key} does not exist.")
    
    def get_name(self):
        name = ''
        if roster_type == 'Player':
            name = self.data[PLAYER_FIRST_NAME_CODE] + ' ' + self.data[PLAYER_LAST_NAME_CODE]
        if roster_type == 'Coach':
            name = self.data[COACH_FIRST_NAME_CODE] + ' ' + self.data[COACH_LAST_NAME_CODE]
        return name


        
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


def main_menu(members, headers, input_csv_path):
    member_index = None
    skill_file = None
    global roster_type
    global skill_members
    global changes
    if (roster_type == "Coach") or (roster_type == "GM"):
        skill_file = find_skill_file(input_csv_path, roster_type)
        skill_headers, skill_members = read_members_from_csv(skill_file)
    while True:
        if (roster_type == 'Player') or (roster_type == 'Coach'):
            print("\nMain Menu:")
            print(f"1. List all {roster_type}s on a team")
            print(f"2. Select a {roster_type} by name")
            print(f"3. Modify all {roster_type}s on a team")
            print(f"4. Randomize {roster_type}s names (warning, this will affect all {roster_type}s!)")
            print("q. Quit")

            choice = input("Enter your choice: ").strip().lower()

            if choice == '1':
                list_roster_by_team(roster_type, members)
            elif choice == '2':
                while True:
                    first_name = input(f"Enter {roster_type}'s first name (or 'q' to quit): ").strip()
                    if first_name.lower() in ['q', 'quit']:
                        break
                    last_name = input(f"Enter {roster_type}'s last name (or 'q' to quit): ").strip()
                    if last_name.lower() in ['q', 'quit']:
                        break
                    member_index = find_member_index(members, first_name, last_name, roster_type)

                    if member_index is not None:
                        modify_roster_member(roster_type, members[member_index])
                        break
                    else:
                        print(f"{roster_type} not found. Please try again.")
            elif choice == '3':
                print_team_names()
                team_id = False
                while True:
                    team_id = input(f"Enter team to bulk edit {roster_type}s (or 'q' to quit): ").strip()
                    if team_id.lower() in ['q', 'quit']:
                        break
                    elif team_id:
                        modify_team_roster(team_id, members)
                        break
            elif choice == '4':
                if roster_type == 'Player':
                    randomize_player_names(members)
                elif roster_type == 'Coach':
                    randomize_coach_names(members)
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
        "Player": ("PLAYER_FIRST_NAME_CODE", "PLAYER_LAST_NAME_CODE"),
        "Coach": ("COACH_FIRST_NAME_CODE", "COACH_LAST_NAME_CODE"),
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


def modify_member(actions, member):
    global skill_members
    global changes
    global roster_type
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

def modify_bulk_members(actions, team_id, members):
    global skill_members
    global changes
    global roster_type
    while True:
        print("Choose an action to perform:")
        for key, (description, _) in actions.items():
            print(f"{key}. {description}")
        print(f"q. Quit to {roster_type} selection")

        choice = input("Enter the number of your choice: ").strip().lower()
        if choice in actions:
            _, action = actions[choice]
            for member in members:
                if member.data['TGID'] == team_id:
                    action(member)
                    changes = True
                    print(f"Action '{actions[choice][0]}' performed on {roster_type} {member.get_name()}.")
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


def modify_team_roster(team_id, members):
    global roster_type
    if roster_type == 'Player':
        modify_all_players_on_team(team_id, members)
    elif roster_type == 'Coach':
        modify_all_coaches_on_team(team_id, members)
    else:
        print("error: no player or coach DBs detected, how did you get here?")


def read_the_manual(member):
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

def inflate_current_stats(member):
    #this will increase the player's stats by half the difference between their current value and the player's potential maximum
    inflated_value = 0
    inflation_amount = 0
    for stat, max in PLAYER_STATS.items():
        player_stat = int(member.data[stat])
        player_stat_max = int(member.data[max])
        if player_stat < player_stat_max:
            inflation_amount = (player_stat_max - player_stat) // 2
        else:
            inflation_amount = 0
        inflated_value = player_stat + inflation_amount
        member.set_stat(stat, inflated_value)


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
            first_name = player.data[PLAYER_FIRST_NAME_CODE]
            last_name = player.data[PLAYER_LAST_NAME_CODE]
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
    #set age to 21
    player.set_stat('PAGE', 21)

    #increase height and weight by 10% each
    current_height = player.data.get('PHGT', 0)
    current_weight = player.data.get('PWGT', 0)
    new_height = int(float(current_height) * 1.1)
    new_weight = int(float(current_weight) * 1.1)
    player.set_stat('PHGT', new_height)
    player.set_stat('PWGT', new_weight)


def modify_all_players_on_team(team_id, players):
    actions = {
        "1": ("Maximize Potential", max_potential),
        "2": ("Maximize Health", max_health),
        "3": ("Resign for Peanuts (7yr contract at league minimum salary)", resign_for_peanuts),
        "4": ("Make Physical Specimen (increase physical size & max potentials)", make_physical_specimen),
        "5": ("Take 'roids (inflate current stats)", inflate_current_stats),
        "6": ("Change Key Value", change_key_value),
    }
    modify_bulk_members(actions, team_id, players)

def modify_player(player):
    actions = {
        "1": ("Maximize Potential", max_potential),
        "2": ("Maximize Health", max_health),
        "3": ("Resign for Peanuts (7yr contract at league minimum salary)", resign_for_peanuts),
        "4": ("Make Physical Specimen (increase physical size & max potentials)", make_physical_specimen),
        "5": ("Take 'roids (inflate current stats)", inflate_current_stats),
        "6": ("Rename Player", rename_player),
        "7": ("Change Key Value", change_key_value),
    }
    modify_member(actions, player)


def randomize_player_names(players):
    global changes
    changes = True
    # Collect all distinct first and last names
    first_name_set = set()
    last_name_set = set()
    
    for player in players:
        if PLAYER_FIRST_NAME_CODE in player.data:
            first_name_set.add(player.data[PLAYER_FIRST_NAME_CODE])
        if PLAYER_LAST_NAME_CODE in player.data:
            last_name_set.add(player.data[PLAYER_LAST_NAME_CODE])
    
    # Convert sets to lists so we can randomly choose from them
    first_names = list(first_name_set)
    last_names = list(last_name_set)
    
    # Randomize each player's name
    for player in players:
        # Select random first and last names
        new_first_name = random.choice(first_names)
        player.set_stat(PLAYER_FIRST_NAME_CODE, new_first_name)
        new_last_name = random.choice(last_names)
        player.set_stat(PLAYER_LAST_NAME_CODE, new_last_name)


def rename_player(player):
    first_name = input("Enter new first name (case-sensitive): ").strip()
    last_name = input("Enter new last name (case-sensitive): ").strip()
    player.set_stat(PLAYER_FIRST_NAME_CODE, first_name)
    player.set_stat(PLAYER_LAST_NAME_CODE, last_name)


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
            first_name = coach.data[COACH_FIRST_NAME_CODE]
            last_name = coach.data[COACH_LAST_NAME_CODE]
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


def modify_all_coaches_on_team(team_id, coaches):
    actions = {
        "1": ("Max General Coaching Potential", max_general_coaching_potential),
        "2": ("Max Positional Coaching Potential", max_positional_coaching_potential),
        "3": ("Read the Manual (Max Skill Points)", read_the_manual),
        "4": ("Take old boy out for drinks (Captain personality)", captain_personality),
        "5": ("Change Key Value", change_key_value),
    }

    modify_bulk_members(actions, team_id, coaches)


def modify_coach(coach):
    actions = {
        "1": ("Max General Coaching Potential", max_general_coaching_potential),
        "2": ("Max Positional Coaching Potential", max_positional_coaching_potential),
        "3": ("Read the Manual (Max Skill Points)", read_the_manual),
        "4": ("Take old boy out for drinks (Captain personality)", captain_personality),
        "5": ("Rename Coach", rename_coach),
        "6": ("Change Key Value", change_key_value),
    }

    modify_member(actions, coach, "Coach")


def randomize_coach_names(coaches):
    global changes
    changes = True
    # Collect all distinct first and last names
    first_name_set = set()
    last_name_set = set()
    
    for coach in coaches:
        if COACH_FIRST_NAME_CODE in coach.data:
            first_name_set.add(coach.data[COACH_FIRST_NAME_CODE])
        if COACH_LAST_NAME_CODE in coach.data:
            last_name_set.add(coach.data[COACH_LAST_NAME_CODE])
    
    # Convert sets to lists so we can randomly choose from them
    first_names = list(first_name_set)
    last_names = list(last_name_set)
    
    # Randomize each player's name
    for coach in coaches:
        # Select random first and last names
        new_first_name = random.choice(first_names)
        coach.set_stat(COACH_FIRST_NAME_CODE, new_first_name)
        new_last_name = random.choice(last_names)
        coach.set_stat(COACH_LAST_NAME_CODE, new_last_name)


def rename_coach(coach):
    first_name = input("Enter new first name (case-sensitive): ").strip()
    last_name = input("Enter new last name (case-sensitive): ").strip()
    coach.data[COACH_FIRST_NAME_CODE] = first_name
    coach.data[COACH_LAST_NAME_CODE] = last_name


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
        "3": ("Read the Manual (Max Skill Points)", read_the_manual),
        "4": ("Take old boy out for drinks (Captain personality)", captain_personality),
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
        "2": ("Read the Manual (Max Skill Points)", read_the_manual),
        "3": ("Take old boy out for drinks (Captain personality)", captain_personality),
        "4": ("Change Key Value", change_key_value),
    }
    modify_member(actions, trainer, 'Trainer')


def rename_trainer(trainer):
    pass # requires PERV file to be dumped in order to implement.


# main()
def main():
    global roster_type
    input_csv_path = get_input_file()

    headers, members = read_members_from_csv(input_csv_path)
    roster_type = detect_roster_type(headers)
    print(f"Detected roster type: {roster_type}")

    main_menu(members, headers, input_csv_path)

if __name__ == "__main__":
    main()
